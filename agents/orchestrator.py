
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logging_setup import setup_logging
setup_logging()


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


    def store_conversation(self,query, answer):
        agent_memory_file = os.path.join(AGENT_MEMORY_DIR, 'memory.json')
        if not os.path.exists(AGENT_MEMORY_DIR):
            os.makedirs(AGENT_MEMORY_DIR)
        data = {}
        if os.path.exists(agent_memory_file):
            with open(agent_memory_file) as f:
                data = json.load(f)
            
        if "previous_conversation" in data:
            if len(data['previous_conversation'])>=5:
                data['previous_conversation'].pop(0)
            data['previous_conversation'].append({"user_question" : query, "response":answer})
        else:
            data['previous_conversation']=[{"user_question" : query, "response":answer}]
        
        with open(agent_memory_file,'w') as f:
            json.dump(data, f)

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
        docs = None
        if query_type in ['NDA', 'SLA', 'DPA']:
            docs = self.retriever.retrieve_full_document(document_type=query_type)
        else:
            stored_query_type = self.get_query_type_from_memory()
            logger.info(f"query_type from memory: {stored_query_type}")
            logger.info("="*50)
            if stored_query_type in ['NDA', 'SLA', 'DPA']:
                docs = self.retriever.retrieve_full_document(document_type=stored_query_type)
                docs_semantic, scores = self.retriever.retrieve(question, document_type=None)
                docs = docs + docs_semantic
        
        if docs==None:
            docs, scores = self.retriever.retrieve(question, document_type=None)

        answer = self.analyzer.analyze(question, docs)
        self.store_conversation(question, answer)

        risk = self.risk_agent.assess(docs)

        citations = self.validator.validate(docs)

        # print(answer)
        # print(risk)
        # print(citations)

        return {
            "answer": answer,
            "risk_level": risk['risk_level'],
            "risk_details":risk['risk_details'],
            "citations": citations
        }

if __name__ == "__main__":

    query_planner = OrchestratorAgent()
    # print(query_planner.prompt)
    answer = query_planner.handle_query("Can Vendor XYZ share Acme’s confidential data with subcontractors?")
    print(answer['answer'])
    print(answer['risk_level'])
    print(answer['risk_details'])
    print(answer['citations'])
    