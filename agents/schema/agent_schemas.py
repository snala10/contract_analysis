from pydantic import BaseModel, Field
from enum import Enum

class RiskRequired(str, Enum):
    yes = "Yes"
    no = "No"

class QueryPlannerSchema(BaseModel):
    legal_topic: str = Field(
        description="The main legal subject or issue discussed in the input text (e.g., termination, liability, confidentiality). only generate the topic",
    )

    risk_analysis_required: str = Field(
        description="Indicates whether a formal legal risk assessment is necessary. Must be 'Yes' or 'No'."
    )

    optimized_search_query: str = Field(
        description="A concise and well-structured legal search query suitable for researching the issue in legal databases."
    )