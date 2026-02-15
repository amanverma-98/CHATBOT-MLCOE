from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

from app.services.llm_service import get_llm
from app.services.retriever_service import retrieve
from app.core.prompts import SYSTEM_PROMPT


# ---------------- STATE ----------------
class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    context: str


# ---------------- RETRIEVE NODE ----------------
def retrieve_node(state: GraphState):
    last_message = state["messages"][-1].content
    context, score = retrieve(last_message)

    return {"context": context}


# ---------------- ROUTER ----------------
def route(state: GraphState):
    if state["context"] is None:
        return "chat"
    return "rag"


# ---------------- CHAT NODE ----------------
def chat_node(state: GraphState):
    llm = get_llm(streaming=False)

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        *state["messages"]
    ])

    return {"messages": [response]}


# ---------------- RAG NODE ----------------
def rag_node(state: GraphState):
    llm = get_llm(streaming=False)

    context = state["context"]
    question = state["messages"][-1].content

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Relevant Context:\n{context}"},
        *state["messages"]
    ])

    return {"messages": [response]}


# ---------------- BUILD GRAPH ----------------
workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("chat", chat_node)
workflow.add_node("rag", rag_node)

workflow.set_entry_point("retrieve")

workflow.add_conditional_edges("retrieve",route, {"chat": "chat", "rag": "rag"})

workflow.add_edge("chat", END)
workflow.add_edge("rag", END)

memory = InMemorySaver()

graph = workflow.compile(checkpointer=memory)