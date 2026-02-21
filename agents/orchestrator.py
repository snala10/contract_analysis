
import sys
import os
from logging_setup import setup_logging

setup_logging()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.query_understander import QueryUnderstanderAgent
from agents.retrieval import RetrievalAgent
from agents.analysis import LegalAnalysisAgent
from agents.risk import RiskAssessmentAgent
from agents.validator import CitationValidatorAgent
from configs import AGENT_MEMORY_DIR
import json
import logging

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    def __init__(self):
        self.planner = QueryUnderstanderAgent()
        self.retriever = RetrievalAgent()
        self.analyzer = LegalAnalysisAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.validator = CitationValidatorAgent()

    def get_query_type_from_memory(self):
        agent_memory_file = os.path.join(AGENT_MEMORY_DIR, 'memory.json')
        data = {}
        if os.path.exists(agent_memory_file):
            with open(agent_memory_file) as f:
                data = json.load(f)
            
        stored_value = data.get('query_type', 'None')
        return stored_value


    def handle_query(self, question):
        logger.info(f"User Query : {question}")
        logger.info("="*50)
        logger.info("Started Query Understander Module")
        qu_output = self.planner.plan(question)
        logger.info(f"User Query Understander Output : {qu_output}")
        logger.info("="*50)
        query_type = qu_output.get('query_type','NA')
        query_type = query_type.strip()
        logger.info(f"query_type from query : {query_type}")
        logger.info("="*50)
        if query_type in ['NDA', 'SLA', 'DPA']:
            docs, scores = self.retriever.retrieve(question, document_type=query_type)
        else:
            stored_query_type = self.get_query_type_from_memory()
            logger.info(f"query_type from memory: {stored_query_type}")
            logger.info("="*50)
            if stored_query_type in ['NDA', 'SLA', 'DPA']:
                docs, scores = self.retriever.retrieve(question, document_type=stored_query_type)
        
        docs, scores = self.retriever.retrieve(question, document_type=None)

        answer = self.analyzer.analyze(question, docs)

        risk = self.risk_agent.assess(docs)

        citations = self.validator.validate(answer, docs)

        # print(answer)
        # print(risk)
        # print(citations)

        return {
            "answer": answer,
            "risk": risk,
            "citations": citations
        }

if __name__ == "__main__":

    query_planner = OrchestratorAgent()
    # print(query_planner.prompt)
    answer = query_planner.handle_query("Can Vendor XYZ share Acme’s confidential data with subcontractors?")
    print(answer['answer'])
    print(answer['citations'])
    