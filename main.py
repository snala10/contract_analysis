from agents.orchestrator import OrchestratorAgent
import os
from configs import AGENT_MEMORY_DIR
import logging
logger = logging.getLogger(__name__)
def main():
    orchestrator = OrchestratorAgent()

    print("Starting Legal Multi-Agent RAG System ")
    print("Type 'exit' to quit.\n")
    agent_memory_file = os.path.join(AGENT_MEMORY_DIR, 'memory.json')
    if os.path.exists(agent_memory_file):
        os.remove(agent_memory_file)
        logger.info(f"{agent_memory_file}  Agent Memory deleted successfully.")
    else:
        logger.info(f"{agent_memory_file} Agent Memory does not exist.")

    while True:
        query = input(">> ")

        if query.lower() in ["exit", "quit"]:
            break

        response = orchestrator.handle_query(query)

        print("\n==============================")
        print("ANSWER:\n", response["answer"])
        risk_level = response["risk_level"]
        risk_level = risk_level.upper()
        if risk_level=="HIGH":
            print("\nRISK ANALYSIS:\n")
            print("\nRISK LEVEL: ", risk_level)
            print("\nRISK DETAILSS: ", response["risk_details"])
        print("\nREFERENCED DOCUMENTS:")
        for c in response["citations"]:
            print("-", c)
        print("================================\n")


if __name__ == "__main__":
    main()