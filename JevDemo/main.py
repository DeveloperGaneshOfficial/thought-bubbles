from turtle import st
from typesafe_sdk import TypeSafeClient, Noul, Choice, Score, NoulCriteria
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import rich
import json
from dotenv import load_dotenv
from client import decide
from routers import AgentRouter
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
        input_query = input("Enter your query: ")
        # with open("inputs.json", "r") as input_json_file:
        #     inputs = json.load(input_json_file)

        # for input_query in inputs["input_queries"]:
        # # input_query = input("Enter your Query:")
        request_state = {**state, "user_query": input_query}
        #     print(f"Input Query: {input_query}")
            # Design notes:
            # - need_tool / need_agent are independent questions. "Both" is derived in code
            #   (need_tool AND need_agent), so the model never has to resolve overlapping questions.
            # - Every question points at state["user_query"] and the descriptions in
            #   tools_available / agents_available, and is phrased as one self-contained question.
            # - Choice options carry descriptions (criteria) and an explicit "none" escape hatch.
        questions={
                "need_tool":Noul(
                    instructions={
                        "question":"Does answering state.user_query require calling at least one tool from state.tools_available "
                                "(e.g. to fetch database records, run code, or get current web information)?",
                        "note":"Judge only on the tool descriptions. Answer false if the query can be answered from general "
                            "knowledge or conversation alone. Ignore whether an agent is also involved.",
                    },
                    criteria={
                        "true":"The query needs live data, computation/execution, or web information that only a tool can provide.",
                        "false":"No tool is needed; the query can be answered without external data or execution.",
                    },
                ),
                "need_agent":Noul(
                    instructions={
                        "question":"Does answering state.user_query benefit from a specialist or support agent from "
                                "state.agents_available (reasoning, analysis, code writing/explanation, or guidance)?",
                        "note":"Judge only on the agent descriptions. Ignore whether a tool is also needed. "
                            "A request that only needs raw data retrieval or a single tool call with no interpretation is false.",
                    },
                    criteria={
                        "true":"The query needs interpretation, analysis, code help, or explanation from an agent.",
                        "false":"The query is a pure tool operation; no agent reasoning is needed.",
                    },
                ),
                "which_agent":Choice(
                    instructions={
                        "question":"Which single agent in state.agents_available is the best fit for state.user_query?",
                        "note":"Pick 'none' if no agent is needed. Choose by the agent's described specialty, not by keyword overlap.",
                    },
                    criteria={
                        "pyCodeZen":"Writing, explaining, debugging or refactoring Python code. Helps with python related queries",
                        "salesPerformanceAnalyzer":"Interpreting sales metrics, trends, comparisons and recommendations.",
                        "supporto":"General conversational help, general-knowledge explanations, step-by-step guidance.",
                        "none":"No agent is needed for this query.",
                    },
                ),
                "which_tool":Choice(
                    instructions={
                        "question":"Which single tool in state.tools_available would be called first for state.user_query?",
                        "note":"Pick 'none' if no tool is needed. If several apply, choose the one needed first.",
                    },
                    criteria={
                        "sql_query":"Retrieve or aggregate records from the private sales database.",
                        "python_code_executor":"Run Python for calculations, transformations or verifying code.",
                        "web_search":"Look up current or external information on the web.",
                        "none":"No tool is needed for this query.",
                    },
                ),
        }

        router_result = await decide(request_state, questions)
        rich.print(router_result)
        print()
        if router_result.nouls["need_agent"].noul > 0.7:
            agent = router_result.choices["which_agent"].choice
            print(f"Agent:{agent}")
            if router_result.nouls["need_tool"].noul > 0.7:
                tool = router_result.choices["which_tool"].choice
                print(f"Tool:{tool}")
        elif router_result.nouls["need_tool"].noul > 0.7:
            tool = router_result.choices["which_tool"].choice
            print(f"Tool: {tool}")
            agent = router_result.choices["which_agent"].choice
            print(f"Agent: {agent}")
        elif router_result.nouls["need_tool"] > 0.7:
            pass

        # print(router_result.nouls["need_agent"], router_result.nouls["need_tool"], router_result.nouls["need_both"])
        # print("toolRouter()") if router_result.nouls["need_tool"].noul > 0.75 else print("agentRouter()")

asyncio.run(main())