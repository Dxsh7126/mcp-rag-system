import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_query = input("Enter query: ")
messages = [{"role":"user","content":user_query}]

async def main():
    # 1. Define how to connect to your server, a note that tells what to do, preparation
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]    # runs your server as a subprocess
    )
    
    # 2. Connect to the server, 
    async with stdio_client(server_params) as (read, write): # "Start the server and give me a way to talk to it" Launches mcp_server.py with 2 pipes read and write
        async with ClientSession(read, write) as session:  #ClientSession wraps the read/write into something easier to use
            await session.initialize() # Like a handshake, "Hey Server, Im here lets talk"
            
            # 3. Discover tools automatically!
            tools_result = await session.list_tools() # What tools do u have?
            print("Available tools:", [t.name for t in tools_result.tools])
            tools_lst=[]
            # 4. MCP tools format of what Groq expects
            for t in tools_result.tools:
                tools_lst.append({
                    "type":"function",
                    "function":{
                        "name":t.name,
                        "description":t.description,
                        "parameters":t.inputSchema
                        }
                })
            
            # 5. Agent loop (same as your agent.py!)
            print("Tools being sent:", json.dumps(tools_lst, indent=2))
            while True:
                response = client_groq.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=tools_lst
                )

                message = response.choices[0].message
                if message.tool_calls:                  # tool_calls is either a list (LLM wants tools) or None (LLM has an answer)
                    messages.append(message)
                    tool_name = message.tool_calls[0].function.name
                    tool_args = message.tool_calls[0].function.arguments
                    args = json.loads(tool_args)
                    result = await session.call_tool(tool_name,args)    # asking the MCP server to run the tools, function ran and result returned
                    result_text = result.content[0].text
                    messages.append({"role":"tool","tool_call_id":message.tool_calls[0].id,"content":result_text})
            #    But instead of calling Python functions directly,
            #    you call: await session.call_tool(tool_name, arguments)
                else:
                    print(message.content)
                    break
asyncio.run(main())
