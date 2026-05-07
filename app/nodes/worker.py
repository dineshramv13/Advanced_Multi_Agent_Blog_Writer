from app.schemas import Task, Plan, EvidenceItem
from app.llm import get_llm  # ✅ changed
from langchain_core.messages import SystemMessage, HumanMessage

import time

# -----------------------------
# Retry Wrapper
# -----------------------------
def safe_llm_call(llm, messages, retries=3):
    """
    Retry wrapper for LLM calls to handle transient failures (502, timeouts, etc.)
    """
    for attempt in range(retries):
        try:
            return llm.invoke(messages).content.strip()
        except Exception as e:
            print(f"[RETRY] attempt {attempt+1} failed: {e}")
            time.sleep(2 * (attempt + 1))  # exponential backoff

    return None  # signals failure


# -----------------------------
# Worker Prompt
# -----------------------------
WORKER_SYSTEM = """You are a senior technical writer and developer advocate.
Write ONE section of a technical blog post in Markdown.

Hard constraints:
- Follow the provided Goal and cover ALL Bullets in order (do not skip or merge bullets).
- Stay close to Target words (±15%).
- Output ONLY the section content in Markdown (no blog title H1, no extra commentary).
- Start with a '## <Section Title>' heading.

Scope guard (prevents mid-blog topic drift):
- If blog_kind == "news_roundup": do NOT turn this into a tutorial/how-to guide.
  Do NOT teach web scraping, RSS, automation, or "how to fetch news" unless bullets explicitly ask for it.
  Focus on summarizing events and implications.

Grounding policy:
- If mode == open_book (weekly news):
  - Do NOT introduce any specific event/company/model/funding/policy claim unless it is supported by provided Evidence URLs.
  - For each event claim, attach a source as a Markdown link: ([Source](URL)).
  - Only use URLs provided in Evidence. If not supported, write: "Not found in provided sources."
- If requires_citations == true (hybrid sections):
  - For outside-world claims, cite Evidence URLs the same way.
- Evergreen reasoning (concepts, intuition) is OK without citations unless requires_citations is true.

Code:
- If requires_code == true, include at least one minimal, correct code snippet relevant to the bullets.

Style:
- Short paragraphs, bullets where helpful, code fences for code.
- Avoid fluff/marketing. Be precise and implementation-oriented.
"""


# -----------------------------
# Worker Node
# -----------------------------
def worker_node(payload: dict) -> dict:

    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]
    topic = payload["topic"]
    mode = payload.get("mode", "closed_book")
    as_of = payload.get("as_of")
    recency_days = payload.get("recency_days")

    # 🔐 NEW: get dynamic LLM using user key
    openrouter_key = payload.get("openrouter_key")
    llm = get_llm(openrouter_key)

    bullets_text = "\n- " + "\n- ".join(task.bullets)

    # Evidence formatting
    evidence_text = ""
    if evidence:
        evidence_text = "\n".join(
            f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}".strip()
            for e in evidence[:20]
        )

    print(f"[START] Worker {task.id}")

    messages = [
        SystemMessage(content=WORKER_SYSTEM),
        HumanMessage(
            content=(
                f"Blog title: {plan.blog_title}\n"
                f"Audience: {plan.audience}\n"
                f"Tone: {plan.tone}\n"
                f"Blog kind: {plan.blog_kind}\n"
                f"Constraints: {plan.constraints}\n"
                f"Topic: {topic}\n"
                f"Mode: {mode}\n"
                f"As-of: {as_of} (recency_days={recency_days})\n\n"
                f"Section title: {task.title}\n"
                f"Goal: {task.goal}\n"
                f"Target words: {task.target_words}\n"
                f"Tags: {task.tags}\n"
                f"requires_research: {task.requires_research}\n"
                f"requires_citations: {task.requires_citations}\n"
                f"requires_code: {task.requires_code}\n"
                f"Bullets:{bullets_text}\n\n"
                f"Evidence (ONLY use these URLs when citing):\n{evidence_text}\n"
            )
        ),
    ]

    result = safe_llm_call(llm, messages)

    if result is None:
        print(f"[ERROR] Worker failed for task {task.id}")
        section_md = f"""## {task.title}

⚠️ This section could not be generated due to a temporary LLM error.
Please try regenerating the blog.
"""
    else:
        section_md = result

    print(f"[END] Worker {task.id}")

    # deterministic ordering
    return {"sections": [(task.id, section_md)]}