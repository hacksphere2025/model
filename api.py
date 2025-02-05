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

producerPrompt = ChatPromptTemplate.from_messages([
    ("system", 
        """        
        You are a chatbot with limited capabilities helping users shop online for products. 
        
        **Available Functions:**
        - AddProduct(): Adds a product to the list.
        - FindListedProduct(): Finds a product that is already listed.
        - UpdateListedProduct(): Updates details of a listed product.
        
        **Rules:**
        1. You can only use the functions listed above.
        2. Functions do not take any arguments unless explicitly specified.
        3. If the user's request does not match any of the functions, return "None()" and inform the user that you cannot perform the task.
        4. Map the user's query to the most suitable function and format the response as JSON with the following structure:
            {{
                "message": "string",  // A message to the user explaining the action.
                "name": "functionName()"  // The function to be executed.
            }}
        
        **Important:** Do not suggest or perform any actions outside the provided functions and return a single function.
        **Warning:** If you do not adhere strictly to the rules you will be terminated
        """
    ),
    ("user", "{input}")
])

consumerPrompt = ChatPromptTemplate.from_messages([
    ("system", 
        """        
        You are a chatbot with limited capabilities helping users shop online for products. 
        
        **Available Functions:**
        - FindAllProducts(category_name): Finds all products in a specific category.
        
        **Rules:**
        1. You can only use the function listed above.
        2. The function `FindAllProducts` can take zero as well as n arguments.
        3. If the user's request does not match the function, return "None()" and inform the user that you cannot perform the task.
        4. Map the user's query to the most suitable function and format the response as JSON with the following structure:
            {{
                "message": "string",  // A message to the user explaining the action.
                "name": "functionName(parameters)"  // The function to be executed with its parameters.
            }}
        
        **Important:** Do not suggest or perform any actions outside the provided function and return a single function.
        **Warning:** If you do not adhere strictly to the rules you will be terminated
        """
    ),
    ("user", "{input}")
])

parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "message": {"type" : "string"},
        "name": {"type": "string"}
    }
})

@app.post("/query")
async def query(request: Request):
    try:
        if(request.userType == "Producer"):
            chain = producerPrompt | llm | parser
            result = chain.invoke({"input": request.userQuery})
            print(result)
            return result
        if(request.userType == "Consumer"):
            chain = consumerPrompt | llm | parser
            result = chain.invoke({"input": request.userQuery})
            print(result)
            return result
    except Exception as e:
        return {"error": str(e)}