from agents.orchestrator import OrchestratorAgent
import os
from configs import AGENT_MEMORY_DIR
import logging
from rich.console import Console
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
        # query = input("Ask Your Query >>> ")
        

        console = Console()

        query = console.input("[bold red]🔍 Ask Your Query >>> [/bold red]")

        if query.lower() in ["exit", "quit"]:
            break

        response = orchestrator.handle_query(query)

        console.print("\n [bold cyan]  ======================================= [/bold cyan] ")
        console.print("\n \n [bold green] ✓ ANSWER : [/bold green]", response["answer"])
        risk_level = response["risk_level"]
        risk_level = risk_level.upper()
        if risk_level=="HIGH":
            print("\nRISK ANALYSIS:\n")
            console.print("\n[bold red] RISK  LEVEL : [/bold red]", risk_level)
            console.print("\n[bold red] RISK  LEVEL : [/bold red] ", response["risk_details"])
        console.print("\n[bold green] REFERENCED DOCUMENTS : [/bold green]\n")
        for i, c in enumerate(response["citations"]):
            print(str(i+1), c)
        console.print("[bold cyan] ========================================= [/bold cyan] \n")


if __name__ == "__main__":
    main()