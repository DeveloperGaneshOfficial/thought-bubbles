from turtle import st
from typesafe_sdk import TypeSafeClient, Noul, Choice, Score, NoulCriteria
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv
from client import decide
load_dotenv()



state = {
    "tools_available": {
        "sql_query": (
            "Queries the sales records database to retrieve, filter, group, and "
            "aggregate stored sales data. Use when an answer requires actual "
            "sales records or database-backed metrics, not general sales advice."
        ),
        "python_code_executor": (
            "Executes Python code and returns its output. Use for numerical "
            "calculations, data transformations, or verifying code behavior. "
            "Writing or explaining code alone does not require execution."
        ),
        "web_search": (
            "Searches the web for current information and external sources. "
            "Use for recent events, up-to-date facts, or research requiring "
            "web sources; it does not access the private sales database."
        ),
    },
    "agents_available": {
        "pyCodeZen": (
            "Python programming specialist for writing, explaining, debugging, "
            "and refactoring Python code. Use for programming assistance; "
            "running code requires the python_code_executor tool separately."
        ),
        "salesPerformanceAnalyzer": (
            "Sales analysis specialist for interpreting sales metrics, comparing "
            "performance, identifying trends, and recommending improvements "
            "based on available data. Retrieving database records requires "
            "the sql_query tool separately."
        ),
        "supporto": (
            "General support agent for conversational help, general knowledge "
            "explanations, and step-by-step guidance that does not require a "
            "Python or sales specialist. Requests needing current external "
            "facts still require web_search."
        ),
    },
}


async def main():
    if __name__=="__main__":

        # console = Console()
        # console.print(Panel.fit("[bold green]Hello[/bold green]", title="This is ChatBot"))
        # input_query = Prompt().ask("Enter Your Query")
        # console.print(Panel( input_query, title="[bold green]Input Query[/bold green]"))
        # input_query = input("Enter your query: ")
        input_query = input("Enter your Query:")
        request_state = {**state, "user_query": input_query}
        questions={
                "need_tool":Noul(
                    instructions={ "question":"Can the user's request be fulfilled by calling one or more tools listed in tools_available, without involving any agent listed in agents_available?"}
                ),
                "need_agent":Noul(instructions={ "question":"Does fulfilling the user's request require assistance from one or more agents listed in agents_available, whether or not tool calls are also needed?"}),
                "need_both":Noul(
                    instructions={"question":"Does fulfilling the user's request require first involving an agent listed in agents_available, which must then invoke one or more tools listed in tools_available to complete the request?"}
                )
        }

        router_result = await decide(request_state, questions)
        print(router_result.nouls["need_agent"], router_result.nouls["need_tool"], router_result.nouls["need_both"])
        # print("toolRouter()") if router_result.nouls["need_tool"].noul > 0.75 else print("agentRouter()")

asyncio.run(main())