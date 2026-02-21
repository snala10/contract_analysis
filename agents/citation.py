class CreateCitation:
    def create_citation(self, documents):
        references = []

        for d in documents:
            source = d.metadata.get("source_document", "Unknown")
            references.append(f"{source}")

        return list(set(references))