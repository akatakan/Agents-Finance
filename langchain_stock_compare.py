from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_ollama import ChatOllama
import yfinance as yf


@tool
def stock_compare(stock: str, stock2: str, year: int) -> str:
    """
    This tool fetches data from Yahoo Finance.
    Args:
        stock: Stock symbol of the first stock for Yahoo Finance
        stock2: Stock symbol of the second stock for Yahoo Finance
        year: Time period to compare like YYYY format as string.
    """
    start_year = f"{year}-01-01"
    end_year = f"{year+1}-01-01"
    first_stock = yf.download(stock,start=start_year,end=end_year)
    second_stock = yf.download(stock2,start=start_year,end=end_year)
    return first_stock, second_stock

tools = [stock_compare]

model_with_tools = ChatOllama(
    model="llama3.1:latest", temperature=0
).bind_tools(tools)

tool_node = ToolNode(tools)

def should_continue(state: MessagesState):
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
    {"messages": [("human", "2024 Yılında altın mı yoksa gümüş mü daha fazla kazandırdı ?.Kâr Farklarını bana göster")]}, stream_mode="values"
):
    chunk["messages"][-1].pretty_print()