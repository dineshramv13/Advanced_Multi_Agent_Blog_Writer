import re
from pathlib import Path
from app.schemas import State 

# -----------------------------
# 8) Reducer (merge + save) — fixed + production-ready
# -----------------------------

def reducer_node(state: State) -> dict:
    # ── 1. Resolve plan ─────────────────────────────────────────────
    plan = state.get("plan")
    if plan is None:
        raise ValueError("Reducer called without a plan.")

    if isinstance(plan, dict):
        blog_title = plan.get("blog_title") or "blog_output"
    else:
        blog_title = getattr(plan, "blog_title", None) or "blog_output"

    # ── 2. Flatten sections ─────────────────────────────────────────
    raw: list = state.get("sections") or []
    parsed: list[tuple[int, str]] = []

    for item in raw:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        try:
            task_id = int(item[0])
            section = str(item[1]).strip() if item[1] is not None else ""
            parsed.append((task_id, section))
        except (ValueError, TypeError):
            continue

    parsed.sort(key=lambda x: x[0])
    body = "\n\n".join(s for _, s in parsed if s).strip()

    final_md = f"# {blog_title}\n\n{body}\n"

    # ── 3. Sanitise filename ────────────────────────────────────────
    safe = re.sub(r'[\\/*?:"<>|]', "", blog_title).strip()
    safe = re.sub(r"\s+", "_", safe) or "blog_output"

    # ── 4. Ensure correct save directory ────────────────────────────
    BLOG_DIR = Path("data/blogs")
    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    out_path = BLOG_DIR / f"{safe}.md"

    # ── 5. Write file with fallback ─────────────────────────────────
    try:
        out_path.write_text(final_md, encoding="utf-8")
        print(f"[SAVED] Blog saved at: {out_path}")
    except OSError as exc:
        fallback_path = BLOG_DIR / "blog_output.md"
        fallback_path.write_text(final_md, encoding="utf-8")
        print(f"[ERROR] Primary save failed ({exc}); saved to {fallback_path}")

    return {"final": final_md}