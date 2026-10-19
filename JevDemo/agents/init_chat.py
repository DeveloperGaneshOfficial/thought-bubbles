from langchain.chat_models import init_chat_model, BaseChatModel
from dotenv import load_dotenv

load_dotenv()

def get_model(model:str="google_genai:gemini-3.5-flash", temperature=0) -> BaseChatModel:
    return init_chat_model(model=model, temperature=temperature)



if __name__ == "__main__":
    print(get_model())