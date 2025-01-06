from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class YFinanceToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    stock: str = Field(..., description="Stock ticker to compare.")
    stock2: str = Field(..., description="Other Stock ticker to compare.")
    year: str = Field(..., description="Time period to compare.")

class YFinanceCompareTool(BaseTool):
    name: str = "Yahoo Finance Tool"
    description: str = (
        "This tool fetches data from Yahoo Finance."
    )
    args_schema: Type[BaseModel] = YFinanceToolInput

    def _run(self, stock: str,stock2:str,year: str) -> str:
        import yfinance as yf
        try:
            start_year = f"{year}-01-01"
            end_year = f"{int(year)+1}-01-01"
            first_stock = yf.download(stock,start=start_year,end=end_year)
            second_stock = yf.download(stock2,start=start_year,end=end_year)
            return first_stock,second_stock
        except Exception as e:
            return f"An error occurred while fetching data: {e}"
