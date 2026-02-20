from pydantic import BaseModel, Field
from enum import Enum

class RiskRequired(str, Enum):
    yes = "Yes"
    no = "No"

class QueryPlannerSchema(BaseModel):
    legal_topic: str = Field(
        description="The main legal subject or issue discussed in the input text (e.g., termination, liability, confidentiality, Indemnification terms, governing_law, Data_breach, compliance ). only generate the topic",
    )

    query_type: str = Field(
        description=(
            "Specifies the type of agreement: Data Processing Agreement (DPA), "
            "Service Level Agreement (SLA), Non-Disclosure Agreement (NDA), or None. "
            "Only return one of: DPA, SLA, NDA, or None."
        )
    )

    risk_analysis_required: str = Field(
        description="Indicates whether a formal legal risk assessment is necessary. Must be 'Yes' or 'No'."
    )

    optimized_search_query: str = Field(
        description="A concise and well-structured legal search query suitable for researching the issue in legal databases."
    )