from mcp.server.fastmcp import FastMCP
import chromadb


client = chromadb.Client()
collection = client.get_or_create_collection(name="my_documents")
file = open("knowledge.txt","r")
content = file.read()


def chunk_text(text,chunk_size,overlap):
        
    chunk_lst=[]
    word_lst = text.split()
    for i in range(0,len(word_lst),chunk_size-overlap):
        chunk_lst.append(" ".join(word_lst[i:i+chunk_size]))
        
    return chunk_lst
chunks = chunk_text(content,50,10)
    #print(chunks)

for index,chunk in enumerate(chunks):
    collection.add(
        ids=[f"doc{index}"],
        documents=[chunk]
    )

# Create the server
mcp = FastMCP("Knowledge Base Server")

# This decorator tells MCP: "this function is a tool"
@mcp.tool()
def search_docs(query: str) -> str:
    """Search the knowledge base for information about distributed computing"""
    
    results = collection.query(query_texts=[query],n_results=3)
    
    # Return the results as a string
    return str(results["documents"])

@mcp.tool()
def calculator(expression: str)-> str:
    """Solve any mathematical questions requested"""
    return str(eval(expression))

# Run the server
if __name__ == "__main__":
    mcp.run()
