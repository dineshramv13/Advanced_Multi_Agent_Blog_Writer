from datetime import date
from app.graph import build_graph

app_graph = build_graph()

def run_blog(topic: str, openrouter_key: str, tavily_key: str):
    result = app_graph.invoke({
        "topic": topic,

        # 🔐 NEW: pass user API keys into graph
        "openrouter_key": openrouter_key,
        "tavily_key": tavily_key,

        "mode": "",
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "plan": None,
        "as_of": date.today().isoformat(),
        "recency_days": 7,
        "sections": [],
        "final": "",
    })

    return result