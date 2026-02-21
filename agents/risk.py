from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from configs import LLM_MODEL
from agents.schema.agent_schemas import RiskAgentSchema
from agents.common_code import LLMCall


class RiskAssessmentAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    def assess(self, documents):
        context = "\n\n".join([d.page_content for d in documents])
        system_prompt =""" You are a legal risk assessment agent."""
        question_prompt = f""" Analyze the clauses below and identify risk exposure.
                Clauses:
                {context}"""
        llm_object = LLMCall()
        
        risk_output=llm_object.get_llm_response(system_prompt, question_prompt, RiskAgentSchema)
        return risk_output
        
        # chain = self.prompt | self.llm
        # return chain.invoke({"context": context}).content