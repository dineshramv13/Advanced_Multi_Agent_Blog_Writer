from langgraph.graph import StateGraph, START, END
from app.schemas import State
from app.nodes.router import router_node, route_next
from app.nodes.research import research_node
from app.nodes.orchestrator import orchestrator_node, fanout
from app.nodes.worker import worker_node
from app.nodes.reducer import reducer_node

def build_graph():
    g = StateGraph(State)

    g.add_node("router", router_node)
    g.add_node("research", research_node)
    g.add_node("orchestrator", orchestrator_node)
    g.add_node("worker", worker_node)
    g.add_node("reducer", reducer_node)

    g.add_edge(START, "router")
    g.add_conditional_edges("router", route_next,
                            {"research": "research", "orchestrator": "orchestrator"})
    g.add_edge("research", "orchestrator")

    g.add_conditional_edges("orchestrator", fanout, ["worker"])
    g.add_edge("worker", "reducer")
    g.add_edge("reducer", END)

    return g.compile()