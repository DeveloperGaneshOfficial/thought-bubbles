from typesafe_sdk import Choice
from langchain.messages import SystemMessage, HumanMessage
from client import decide
from agents import init_chat



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




async def AgentRouter(query):

    request_state = {**state, "user_query":query}

    questions = {
        "agent":Choice(instructions="choose the best agent for given query", criteria={"supporto":None, "salesPerformanceAnalyzer":None, "pyCodeZen":None})
    }

    decision = await decide(request_state, questions)

    print(decision)





if __name__=="__main__":
    import asyncio
    asyncio.run(AgentRouter("write a python program for fibonacci series"))

#     llm_router = init_chat.get_model()
#     res = llm_router.invoke([SystemMessage(content="""You are a Agent Chooser for given query. 
#     ```json 
#     {
#         "agents_available": {
#             "pyCodeZen": (
#                 "Python programming specialist for writing, explaining, debugging, "
#                 "and refactoring Python code. Use for programming assistance; "
#                 "running code requires the python_code_executor tool separately."
#             ),
#             "salesPerformanceAnalyzer": (
#                 "Sales analysis specialist for interpreting sales metrics, comparing "
#                 "performance, identifying trends, and recommending improvements "
#                 "based on available data. Retrieving database records requires "
#                 "the sql_query tool separately."
#             ),
#             "supporto": (
#                 "General support agent for conversational help, general knowledge "
#                 "explanations, and step-by-step guidance that does not require a "
#                 "Python or sales specialist. Requests needing current external "
#                 "facts still require web_search."
#             )
#         }
# }```"""), HumanMessage(content="write a python program for fibonacci series")])


#     import pdb; pdb.set_trace()
#     print(res)