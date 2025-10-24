import os
import asyncio
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()  # Add this line at the top


async def main():
    query = "What is nodejs?"
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-large',
        api_key=os.getenv('OPENAI_API_KEY')
    )
 

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url='http://localhost:6333',
        collection_name='srinibas-collection',
    )
    
    vector_searcher = vector_store.as_retriever(
        search_kwargs={'k': 3}
    )

    relevant_chunks = vector_searcher.invoke(query)

    # Format context from relevant chunks
    context = "\n\n".join([
        f"Content: {doc.page_content}\nMetadata: {doc.metadata}"
        for doc in relevant_chunks
    ])

    SYSTEM_PROMPT = f"""You are an AI Assistant who helps 
in fetching relevant information from the content available to you in the form of PDF file.
Also return the page no with the content you are referring to.

Context:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-5", 
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())