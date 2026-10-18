from typesafe_sdk import Choice
from pydantic import BaseModel





def AgentRouter():
    state = {
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
            )
        }
    }

    questions = {
        "agent":Choice(instructions="", criteria={})
    }