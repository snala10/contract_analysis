from pydantic import BaseModel, Field
from enum import Enum



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

    # optimized_search_query: str = Field(
    #     description="A concise and well-structured legal search query suitable for researching the issue in legal databases."
    # )

class RiskAgentSchema(BaseModel):
    risk_level : str = Field(description="Risk Level: LOW / MEDIUM / HIGH")
    risk_details : str = Field(description="Risk Factors: keep it brief only 2-3 lines.")