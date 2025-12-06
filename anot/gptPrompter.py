from openai import OpenAI
import asyncio
import base64
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

client = OpenAI()

model = ChatOpenAI(
    model = "gpt-4o",
    # temperature= "0.1",
    max_completion_tokens= 1000,
    timeout = 30, 
    streaming= True
)

prompt = '''
First, detect all bounding boxes.
Second, for each bounding box call annotTool(x1, y1, x2, y2).
output only coordinates in json format and label each figure with appropriate label.
output valid Json only in format: 
```json
[
    {"x1": 34, "y1": 55, "x2": 509, "y2": 480},
    {"x1": 524, "y1": 41, "x2": 979, "y2": 467}
]
```
'''

async def main(image_path: str = "input_image/image_resized.png", prompt: str = prompt, stream_chunk=None):
    server_params = StdioServerParameters(  
         command="python",
         args=["mcpServer/annotTool.py"],
    )

    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
    except Exception as e:
        print(f"Error reading image file: {e}")
        return

    img_base64 = base64.b64encode(img_data).decode('utf-8')
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
             await session.initialize()
             tools = await load_mcp_tools(session)
             response = await query_output(prompt, img_base64, tools, stream_chunk)

    return response


async def query_output(prompt, img_base64, tools, stream_chunk):
    agent = create_agent(
        model,
        tools
    )

    msg = {"messages": {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_base64}"
                }}
        ]
    }}
    response_text = agent.astream(msg)


    async for chunk in response_text:
        # print(chunk)
        if "model" in chunk and "messages" in chunk["model"]:
            ai_msg = chunk["model"]["messages"][-1]
            if ai_msg.content:
                final_output = ai_msg.content
                print(final_output)

    # return response_text["output"]

if __name__ == "__main__":
    asyncio.run(main())