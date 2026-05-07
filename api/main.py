from fastapi import FastAPI
from app.runner import run_blog
from pathlib import Path
from fastapi import HTTPException

from pydantic import BaseModel


app = FastAPI()


class BlogRequest(BaseModel):
    topic: str
    openrouter_key: str
    tavily_key: str

BLOG_DIR = Path("data/blogs")
BLOG_DIR.mkdir(parents=True, exist_ok=True)



@app.post("/generate")
def generate_blog(payload: dict):
    try:
        topic = payload.get("topic")
        openrouter_key = payload.get("openrouter_key")
        tavily_key = payload.get("tavily_key")

        result = run_blog(topic, openrouter_key, tavily_key)

        return {"content": result["final"]}

    except Exception as e:
        error_msg = str(e)

        # ✅ Detect Tavily missing case
        if "tavily" in error_msg.lower() or "api key" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="Tavily API key required for this topic"
            )

        raise HTTPException(
            status_code=500,
            detail=error_msg
        )


@app.get("/blogs")
def list_blogs():
    files = [f.name for f in BLOG_DIR.glob("*.md")]
    return {"blogs": files}


@app.get("/blog/{filename}")
def get_blog(filename: str):
    file_path = BLOG_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"content": file_path.read_text(encoding="utf-8")}