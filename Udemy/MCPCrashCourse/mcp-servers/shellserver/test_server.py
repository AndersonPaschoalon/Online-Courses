import asyncio
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import ClientSession, StdioServerParameters


async def test():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            # handshake
            await session.initialize()

            # listar tools
            tools = await session.list_tools()
            print("TOOLS:", tools)

            # chamar tool
            result = await session.call_tool("run_command", {"command": "echo hello"})

            print("RESULT:", result)


asyncio.run(test())
