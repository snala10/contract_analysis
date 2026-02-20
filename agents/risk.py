from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import LLM_MODEL


class RiskAssessmentAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

        self.prompt = ChatPromptTemplate.from_template("""
You are a legal risk assessment agent.

Analyze the clauses below and identify risk exposure.

Clauses:
{context}

Return:
Risk Level: LOW / MEDIUM / HIGH
Risk Factors:
- ...
""")

    def assess(self, documents):
        context = "\n\n".join([d.page_content for d in documents])
        chain = self.prompt | self.llm
        return chain.invoke({"context": context}).content