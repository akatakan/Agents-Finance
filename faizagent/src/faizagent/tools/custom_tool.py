from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class CompoundedInterestToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    amount: float = Field(..., description="initial amount of money")
    time: float = Field(..., description="length of time the money is invested")
    n: int = Field(..., description="number of times interest is compounded per year")
    rate: int = Field(..., description="compound interest rate")

class CompoundedInterestTool(BaseTool):
    name: str = "Compound Interest Calculator"
    description: str = (
        "Calculates compound interest according to the entered principal, interest rate and the number of months interest will be held."
    )
    args_schema: Type[BaseModel] = CompoundedInterestToolInput

    def _run(self, amount: float,rate: int,n: int,time: float) -> str:
        son_para= amount*(1+(rate/100)/n)**(n*(time/12))
        return f"{son_para:.2f}"
