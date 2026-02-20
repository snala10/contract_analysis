# from agents.orchestrator import OrchestratorAgent

def main():
    # orchestrator = OrchestratorAgent()

    print("Legal Multi-Agent RAG System")
    print("Type 'exit' to quit.\n")

    while True:
        query = input(">> ")

        if query.lower() in ["exit", "quit"]:
            break

        # response = orchestrator.handle_query(query)

        print("\n==============================")
        # print("ANSWER:\n", response["answer"])
        # print("\nRISK ANALYSIS:\n", response["risk"])
        # print("\nREFERENCED DOCUMENTS:")
        # for c in response["citations"]:
        #     print("-", c)
        print("==============================\n")


if __name__ == "__main__":
    main()