import os
import json
import re
from prompts.prompts import consumerPrompt, producerPrompt
from fastapi import FastAPI
from groq import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import dotenv

dotenv.load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Groq API key is missing. Set it in the .env file.")

class Request(BaseModel):
    userType: str
    userQuery: str
    session: list | None = None  
app = FastAPI()

llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7,
    api_key=GROQ_API_KEY  
)

@app.post("/query")
async def query(request: Request):
    try:
        session_data = request.session if request.session else []
        history = "\n".join([
            f"Bot: {entry['response']['message']}" 
            for entry in session_data if 'response' in entry
        ])
        full_prompt = f"{history}\nUser: {request.userQuery}"  

        if request.userType == "Producer":
            chain = producerPrompt | llm 
        elif request.userType == "Consumer":
            chain = consumerPrompt | llm 
        else:
            return {"error": "Invalid userType. Must be 'Producer' or 'Consumer'."}
        
        result = chain.invoke({"input": full_prompt})

        try:
            response_data = json.loads(result.content) 
        except json.JSONDecodeError:
            return {"error": "LLM response is not valid JSON", "raw_response": result.content}

        return {"response": response_data}
    except Exception as e:
        return {"error": str(e)}
