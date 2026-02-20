import os
import re
from langchain_core.documents import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import hashlib
from configs import EMBEDDING_MODEL, CHROMA_PERSIST_DIR


def get_doc_id(doc):
    # doc is lanchain Document
    return hashlib.md5(doc.page_content.encode("utf-8")).hexdigest()


def load_text_documents(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, file)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Try clause-based splitting first
        print("file path = ", file_path)
        clauses = split_by_clauses(text)
        document_title = file.replace(".txt","") # file name can be considered as document title
        document_header = clauses[0] # first item in the clauses list is header of the document
        # Print each clause
        # for i, clause in enumerate(clauses, start=1):
        #     print(f"Clause {i}:\n{clause}\n{'-'*50}")

        for idx, clause in enumerate(clauses):
            documents.append(
                Document(
                    page_content=clause.strip(),
                    metadata={
                        "source_document": file,
                        "clause_index": idx,
                        "document_title":document_title,
                        "document_header" : document_header
                    }
                )
            )

    return documents


def split_by_clauses(text):
    """
    Splits text by common legal clause patterns:
    - 1.
    - 1.1
    """

    pattern = r"(?m)^\d+\.\s+"
    clauses = re.split(pattern, text)

    clauses = [clause.strip() for clause in clauses if clause.strip()]

    

    # Merge headings back with content
    # clauses = []
    # buffer = ""

    # for part in splits:
    #     if re.match(pattern, part):
    #         if buffer:
    #             clauses.append(buffer)
    #         buffer = part
    #     else:
    #         buffer += part

    # if buffer:
    #     clauses.append(buffer)

    # # Fallback to full text if split too small
    # if len(clauses) < 3:
    #     splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=800,
    #         chunk_overlap=100
    #     )
    #     return splitter.split_text(text)

    return clauses


def build_vectorstore(documents):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # vectorstore = Chroma.from_documents(
    #     documents,
    #     embedding=embeddings,
    #     persist_directory=CHROMA_PERSIST_DIR
    # )
    ids = [get_doc_id(doc) for doc in documents]
    vector_store = Chroma(
                    collection_name="acme_vendor",
                    embedding_function=embeddings,
                    persist_directory=CHROMA_PERSIST_DIR)
   
    vector_store.add_documents(documents, ids=ids)

    # vectorstore.persist()
    print("✅ Vectorstore built from text files.")
    print("Number of original document:", len(documents))
    print("Number of documents stored:", vector_store._collection.count())
    # return vector_store


if __name__ == "__main__":
    docs = load_text_documents("./data")
    # for doc in docs:
    #     print(f"Clause {doc.metadata['source_document']}:\n{doc.page_content}\n{'-'*50}")
    build_vectorstore(docs)