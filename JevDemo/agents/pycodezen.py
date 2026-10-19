from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel, Field
from init_chat import get_model


class Response(BaseModel):
    input: str = Field(description="Input given to the model")
    type: str = Field(description="Answer Type non-code or code")
    explanation: str = Field(description="A brief description of what the code does")
    code: str = Field(description="The raw executable Python code in markdown")

py_code_zen = create_agent(
    model = get_model(temperature=1),
    system_prompt="""You're an expert python engineer with 10 years of experience.
    Your job is to help user to write and review codes.""",
    response_format=Response,
)


if __name__=="__main__":
    query = input("Enter Query for PyCodeZen Agent:")
    response = py_code_zen.invoke({"messages":HumanMessage(content=query)})
    import pdb; pdb.set_trace()
    print(response)