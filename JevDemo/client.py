from typesafe_sdk import AsyncTypeSafeClient, JSONContent, Questions
from dotenv import load_dotenv
from utils import saveResult
load_dotenv()

async def decide(state:JSONContent, questions:Questions, save_result:bool=True):
    async with AsyncTypeSafeClient() as client:
        result = await client.system_one(state=state, questions=questions)
        if save_result:
            saveResult(result)
        return result