from agents.query_understander import QueryUnderstanderAgent
from agents.retrieval import RetrievalAgent
from agents.analysis import LegalAnalysisAgent
from agents.risk import RiskAssessmentAgent
from agents.validator import CitationValidatorAgent


class OrchestratorAgent:
    def __init__(self):
        self.planner = QueryUnderstanderAgent()
        self.retriever = RetrievalAgent()
        self.analyzer = LegalAnalysisAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.validator = CitationValidatorAgent()

    def handle_query(self, question):
        plan = self.planner.plan(question)

        docs = self.retriever.retrieve(question)

        answer = self.analyzer.analyze(question, docs)

        risk = self.risk_agent.assess(docs)

        citations = self.validator.validate(answer, docs)

        return {
            "answer": answer,
            "risk": risk,
            "citations": citations
        }