from openai import OpenAI
from configs import LLM_MODEL, OPENAI_API_KEY
import json


class LLMCall:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def get_llm_response(self,system_prompt, input_query, pydantic_schema):

        completion = self.client.chat.completions.parse(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": input_query}
                ],
                response_format=pydantic_schema    
            )
        response_data = json.loads(completion.choices[0].message.content)
        return response_data