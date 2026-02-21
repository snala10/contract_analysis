import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pathlib import Path
from configs import EMBEDDING_MODEL, CHROMA_PERSIST_DIR

class RetrievalAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = Chroma(
            collection_name="acme_vendor",
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings
        )

    def retrieve_full_document(self, document_type):
        document_type_mapping = {
        'DPA': ["data_processing_agreement.txt"],
        'SLA':["service_level_agreement.txt", "vendor_services_agreement.txt"],
        'NDA' : ["nda_acme_vendor.txt"]
                                }
        
        current_file = Path(__file__).resolve()
        # Go to parent directory
        project_root = current_file.parent.parent
        data_path = 'data'
        full_document = ""
        for file in document_type_mapping[document_type]:
            file_path = os.path.join(project_root,data_path,file)
            with open(file_path, encoding='utf-8') as f:
                full_document = full_document + f.read()
        
        source = ",".join(document_type_mapping[document_type])
        return [ Document(
                page_content=full_document.strip(),
                metadata={
                    "source_document": source,
                    "clause_index": 0,
                    "document_type": document_type,
                    "document_title":"NA",
                    "document_header" : "NA"})]
    

    def retrieve(self, query, document_type=None, k=2):
        if document_type==None:
            docs = self.vector_store.similarity_search_with_score(query, k=k)
            
        else:
            docs = self.vector_store.similarity_search_with_score(query, k=k, filter={'document_type':document_type})
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
    # docs = retrival_agent.vector_store._collection.get(include=["metadatas", "documents", "embeddings"])

    # # Print each document
    # count = 0
    # for doc_text, meta in zip(docs["documents"], docs["metadatas"]):
    #     # print(f"ID: {doc_id}")
    #     print(f"Metadata: {meta['source_document']}")
    #     print(f"Document Type: {meta['document_type']}")
    #     print(f"Content: {doc_text[:10]}...")  # print first 200 characters
    #     print("-"*50)
    #     count+=1
    # print("Total Documents stored : ", count)
    # for doc in docs:
    #     print(f"Clause {doc.metadata['source_document']}:\n{doc.page_content}\n{'-'*50}")
    # docs, scores = retrival_agent.retrieve("what is the contract termination condition")
    # for i,doc in enumerate(docs):
    #     print(doc.page_content, scores[i])

    print(retrival_agent.retrieve_full_document('NDA'))