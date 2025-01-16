from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_ollama import ChatOllama
import matplotlib.pyplot as plt

@tool
def compounded_interest(amount: float, rate: int, time: int, n: int = 12) -> str:
    """
    Calculates compound interest with monthly compounding by default.
    Args:
        amount: Principal amount
        rate: Annual interest rate as percentage
        time: Time period in months
        n: Number of times interest is compounded per year (default=12 for monthly)
    """
    return f"{amount*(1+(rate/100)/n)**(n*(time/12)):.2f}"

tools = [compounded_interest]

model_with_tools = ChatOllama(
    model="llama3.1:latest", temperature=0
).bind_tools(tools)

tool_node = ToolNode(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    """
    Determines if the conversation should continue to tools or end.
    """
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

for chunk in app.stream(
    {"messages": [("human", "Aylık %3 faizle 10000 TL 6 ay sonra ne kadar olur ?")]}, stream_mode="values"
):
    chunk["messages"][-1].pretty_print()