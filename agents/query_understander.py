from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import LLM_MODEL, AGENT_MEMORY_DIR

import re

from agents.schema.agent_schemas import QueryPlannerSchema
from agents.common_code import LLMCall
import json


class QueryUnderstanderAgent:

    def plan(self, question):
        system_prompt = """
                You are a legal query planning agent. Extract Information from User Query                                                  
                """
        llm_object = LLMCall()
        query_planner_output=llm_object.get_llm_response(system_prompt, question, QueryPlannerSchema)
        self.update_agent_memory(query_planner_output)
        return query_planner_output
    
    
    def update_memory(self, key, value):
        agent_memory_file = os.path.join(AGENT_MEMORY_DIR, 'memory.json')
        if not os.path.exists(AGENT_MEMORY_DIR):
            os.makedirs(AGENT_MEMORY_DIR)
        data = {}
        if os.path.exists(agent_memory_file):
            with open(agent_memory_file) as f:
                data = json.load(f)
            
        stored_value = data.get(key, 'None')

        if value in ['NDA', 'SLA', 'DPA']:
            data[key]=value
        
        with open(agent_memory_file,'w') as f:
            json.dump(data, f)


    def update_agent_memory(self, qu_output):
        if "query_type" in qu_output:
            query_type = qu_output['query_type']
            query_type = query_type.strip()
            query_type = query_type.upper()
            #if query_type in ['NDA', 'SLA', 'DPA']:
            self.update_memory('query_type',query_type)
        
        
if __name__ == "__main__":

    query_planner = QueryUnderstanderAgent()
    # print(query_planner.prompt)
    qu_output = query_planner.plan("What is the notice period for terminating the NDA?")
    if "query_type" in qu_output:
        print(qu_output["query_type"])
    print(qu_output)
    