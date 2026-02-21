from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from configs import LLM_MODEL, AGENT_MEMORY_DIR
import os
import json


class LegalAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

        self.prompt_with_previous_conversation = ChatPromptTemplate.from_template("""
You are a legal contract analysis expert.

Answer the user's question using  the provided clauses and previous conversation. Make use of previous conversation only when
it is absolutely required otherwise ignore it.

Previous Conversation:
{previous_conversation}
                                                       
Question:
{question}

Clauses:
{context}
                                                       
Provide:
- Clear and brief answer to the user query 
- Reference clause sections
""")

    def get_previous_conversation(self):
        agent_memory_file = os.path.join(AGENT_MEMORY_DIR, 'memory.json')
        if not os.path.exists(AGENT_MEMORY_DIR):
            os.makedirs(AGENT_MEMORY_DIR)
        data = {}
        if os.path.exists(agent_memory_file):
            with open(agent_memory_file) as f:
                data = json.load(f)
        if "previous_conversation" in data:
            conversation = ""
            for item in data["previous_conversation"]:
                conversation+= "User Question : " + item["user_question"] + "\n"
                conversation+= "Response : " + item["response"] + "\n"
            return conversation
        else:
            return "No Previous Conversation Available"

    def analyze(self, question, documents):
        context = "\n\n".join([d.page_content for d in documents])
        previous_conversation = self.get_previous_conversation()
        chain = self.prompt_with_previous_conversation | self.llm
        return chain.invoke({
            "previous_conversation": previous_conversation,
            "question": question,
            "context": context
        }).content