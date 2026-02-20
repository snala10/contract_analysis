from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from configs import LLM_MODEL


class LegalAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

        self.prompt = ChatPromptTemplate.from_template("""
You are a legal contract analysis expert.

Answer the user's question using ONLY the provided clauses.

Question:
{question}

Clauses:
{context}

Provide:
- Clear answer
- Reference clause sections
- Do not hallucinate
""")

    def analyze(self, question, documents):
        context = "\n\n".join([d.page_content for d in documents])
        chain = self.prompt | self.llm
        return chain.invoke({
            "question": question,
            "context": context
        }).content