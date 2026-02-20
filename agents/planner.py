from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import LLM_MODEL

import re

class QueryPlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

        self.prompt = ChatPromptTemplate.from_template("""
You are a legal query planning agent.

Analyze the user question and extract:
Legal topic (termination, liability, indemnification, etc.)
Whether risk analysis is required (Yes/No)
Optimized search query

User Question:
{question}

Return structured output                                                    
""")

    def plan(self, question):
        chain = self.prompt | self.llm
        output = chain.invoke({"question": question}).content
        output_dict=self.extract_json(output)
        return output_dict

    def extract_json(self, output_string):
        pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"'

        matches = re.findall(pattern, output_string)
        output_dict = {}

        for key, value in matches:
            output_dict[key.lower()]=value
            print("Key:", key)
            print("Value:", value)
            print("---")
        return output_dict


if __name__ == "__main__":

    query_planner = QueryPlannerAgent()
    # print(query_planner.prompt)
    print(query_planner.plan("What is the notice period for terminating the NDA?"))
    