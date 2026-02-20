import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from configs import EMBEDDING_MODEL, CHROMA_PERSIST_DIR

class RetrievalAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = Chroma(
            collection_name="acme_vendor",
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings
        )

    def retrieve(self, query, k=3):
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        # docs will tuple where first element will be Document Object 
        # and second element will be similarity score

        # Sort by similarity score (lower = better in Chroma)
        docs = sorted(docs, key=lambda x: x[1])
        document = [doc[0] for doc in docs]
        scores = [doc[1] for doc in docs]
        return document, scores


if __name__ == "__main__":

    """ Test Retrieval Agent By Running this script"""
    retrival_agent = RetrievalAgent()
    docs = retrival_agent.vector_store._collection.get(include=["metadatas", "documents", "embeddings"])

    # Print each document
    count = 0
    for doc_text, meta in zip(docs["documents"], docs["metadatas"]):
        # print(f"ID: {doc_id}")
        print(f"Metadata: {meta['source_document']}")
        print(f"Content: {doc_text[:100]}...")  # print first 200 characters
        print("-"*50)
        count+=1
    print("Total Documents stored : ", count)
    # for doc in docs:
    #     print(f"Clause {doc.metadata['source_document']}:\n{doc.page_content}\n{'-'*50}")
    # docs = retrival_agent.retrieve("what is the contract termination condition")
    # for doc in docs:
    #     print(doc[0].page_content, doc[1])