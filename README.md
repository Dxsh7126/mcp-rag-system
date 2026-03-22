# MCP Powered RAG Agent

This is a project that uses multiple tools such as search_docs and calculator tools, it finds information in any document provided and does simple calculation.

## What I Built

2-3 sentences explaining:
- The system is an agent that answers queries from the document provided.
- It works using RAG (retrieval augmented generation) and uses the concept of MCPs. A server is created which holds the tools and the client access those tools based on the query requested by the user.
- Tech used are,

- Python
- Groq
- MCPs
- RAG
- JSON
- LLMs
- APIs

## Architecture

Explain the two main files:
- [mcp_server.py] is the server of the MCP, it contains the different tools that are used by the client. It contains the chunking logic where the document is chunked to smaller pieces for easier and faster processing. Two tools are created, search_docs and calculator, the client can access these tools.
- [mcp_client.py] is the client side of the MCP, it runs the MCP server. The developer configures which servers to connect to and the agent sees which tools are available to it from the server. It asks each configured server to list the tools. The complete list of the tools are returned and the tools that are required for the task is used and final output is returned.


Architecture of how the converstation works between the client and server.
┌─────────────────┐          ┌─────────────────┐
│     CLIENT      │          │      Server     │
│  (your agent)   │          │  (tool provider)│
│                 │  connect │                 │
│  1. Connect ────┼─────────►│                 │
│                 │          │                 │
│  2. "What tools │  list    │                 │
│     do you      │◄─────────┤  search_docs    │
│     have?"      │          │  calculator     │
│                 │          │                 │
│  3. User asks   │  call    │                 │
│     question    │─────────►│  runs tool      │
│                 │  result  │                 │
│  4. Get result  │◄─────────┤  returns answer │
└─────────────────┘          └─────────────────┘


## Key Concepts Used

The key concepts used to create this project are as follows,
- Retrieval-Augmented Generation (RAG)
- Vector embeddings & ChromaDB
- Document chunking with overlap
- AI Agent loop (Think → Act → Observe)
- LLM function calling / tool use
- Model Context Protocol (MCP)

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your `GROQ_API_KEY`
4. Run: `python mcp_client.py`

## Example

Enter query: What are the disadvantages of Three tier architecture?


The disadvantages of Three-tier architecture are:

1. Increased complexity
2. Complexity to manage
3. Security challenges
4. Point of failure

Note: The response from the search function provides information on the disadvantages of Three-tier architecture, as well as other related concepts in distributed computing.