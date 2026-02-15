from langchain_core.messages import HumanMessage, AIMessage
from app.graph.graph_builder import graph

async def generate_stream(question: str, session_id: str):
    """
    Stream response using graph.
    """
    config = {"configurable": {"thread_id": session_id}}

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=question)]},
        config=config
    )

    # Get last AIMessage
    final_msg = result["messages"][-1]
    if isinstance(final_msg, AIMessage):
        yield final_msg.content