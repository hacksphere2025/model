from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import JsonOutputParser
from prompts.prompts import consumerPrompt, producerPrompt
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver

class Request(BaseModel):
    userType: str
    userQuery: str

app = FastAPI()

llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7
)

parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "message": {"type" : "string"},
        "name": {"type": "string"}
    }
})

memory = ConversationBufferMemory()

def call_model(state: MessagesState):
    trimmed_messages = state["messages"]
    system_prompt = (
        "You are a helpful assistant. "
        "Answer all questions to the best of your ability."
    )
    messages = [SystemMessage(content=system_prompt)] + trimmed_messages
    response = llm.invoke(messages)
    return {"messages": response}

workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

memory_saver = MemorySaver()
app_workflow = workflow.compile(checkpointer=memory_saver)

@app.post("/query")
async def query(request: Request):
    try:
        if request.userType == "Producer":
            prompt = producerPrompt
        elif request.userType == "Consumer":
            prompt = consumerPrompt
        else:
            return {"error": "Invalid userType"}

        state = {"messages": [HumanMessage(content=request.userQuery)]}
        result = app_workflow.invoke(state, config={"configurable": {"thread_id": "1"}})
        return {
            "message" : str(result["messages"][-1].content)
        }
    except Exception as e:
        return {"error": str(e)}