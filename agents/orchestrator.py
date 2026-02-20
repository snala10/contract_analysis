from query_understander import QueryUnderstanderAgent
from retrieval import RetrievalAgent
from analysis import LegalAnalysisAgent
from risk import RiskAssessmentAgent
from validator import CitationValidatorAgent


class OrchestratorAgent:
    def __init__(self):
        self.planner = QueryUnderstanderAgent()
        self.retriever = RetrievalAgent()
        self.analyzer = LegalAnalysisAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.validator = CitationValidatorAgent()

    def handle_query(self, question):
        plan = self.planner.plan(question)

        docs, scores = self.retriever.retrieve(question)

        answer = self.analyzer.analyze(question, docs)

        risk = self.risk_agent.assess(docs)

        citations = self.validator.validate(answer, docs)

        print(answer)
        print(risk)
        print(citations)

        return {
            "answer": answer,
            "risk": risk,
            "citations": citations
        }

if __name__ == "__main__":

    query_planner = OrchestratorAgent()
    # print(query_planner.prompt)
    print(query_planner.handle_query("Identify any clauses that could pose financial risk to Acme Corp."))
    