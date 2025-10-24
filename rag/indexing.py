import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

async def init():
    # Load environment variables
    load_dotenv()
    
    # PDF file path
    pdf_file_path = 'rag/myDoc.pdf'
    
    # Load PDF page by page
    loader = PyPDFLoader(pdf_file_path)
    docs = await loader.aload()
    
    # Initialize OpenAI Embedding Model
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-large',
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Create Qdrant client
    client = QdrantClient(url='http://localhost:6333')
    
    # Create vector store from documents
    vector_store = await QdrantVectorStore.afrom_documents(
        docs,
        embeddings,
        url='http://localhost:6333',
        collection_name='srinibas-collection'
    )
    
    print('Indexing of documents done...')

# Run the async function
if __name__ == '__main__':
    import asyncio
    asyncio.run(init())