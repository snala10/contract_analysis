from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import LLM_MODEL

import re

from schema.agent_schemas import QueryPlannerSchema
from common_code import LLMCall
import json


class QueryUnderstanderAgent:

    def plan(self, question):
        system_prompt = """
                You are a legal query planning agent. Extract Information from User Query                                                  
                """
        llm_object = LLMCall()
        query_planner_output=llm_object.get_llm_response(system_prompt, question, QueryPlannerSchema)
        # print(query_planner_output)
        
        return query_planner_output


if __name__ == "__main__":

    query_planner = QueryUnderstanderAgent()
    # print(query_planner.prompt)
    print(query_planner.plan("Is liability capped for breach of confidentiality?"))
    