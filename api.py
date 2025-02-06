import json
import re
from prompts.prompts import consumerPrompt, producerPrompt
from fastapi import FastAPI
from groq import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class Request(BaseModel):
    userType: str
    userQuery: str

app = FastAPI()

llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7
)


@app.post("/query")
async def query(request: Request):
    try:
        if(request.userType == "Producer"):
            chain = producerPrompt | llm 
            result = chain.invoke({"input": request.userQuery})
            print(result)
            content = result.content   
            fixed_content = re.sub(r'\\_', '_', content)
            return json.loads(fixed_content)
        if(request.userType == "Consumer"):
            chain = consumerPrompt | llm 
            result = chain.invoke({"input": request.userQuery})
            print(result)
            content = result.content   
            fixed_content = re.sub(r'\\_', '_', content)
            return json.loads(fixed_content)
    except Exception as e:
        return {"error": str(e)}