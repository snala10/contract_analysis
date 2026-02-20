class CitationValidatorAgent:
    def validate(self, answer, documents):
        references = []

        for d in documents:
            source = d.metadata.get("source_document", "Unknown")
            clause = d.metadata.get("clause_index", "N/A")

            references.append(f"{source} - Clause {clause}")

        return list(set(references))