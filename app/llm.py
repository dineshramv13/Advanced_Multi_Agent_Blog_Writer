from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# Dynamic LLM factory
# -----------------------------
def get_llm(api_key: str) -> ChatOpenAI:
    """
    Returns a ChatOpenAI instance using user-provided API key
    """
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model="openrouter/owl-alpha"
    )