from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from uuid import uuid4
from schemas import JsonRpcRequest, JsonRpcResponse, JsonRpcError, ResponseMessage, MessagePart, ResponseStatus, A2AMessage, Artifact
from fact_checker_agent import FactCheckerAgent

load_dotenv()

app = FastAPI(
    title="Fact Checker Agent",
    description="Your very own smart-ass colleague",
    version="1.0.0"
       )

fact_checker = FactCheckerAgent()

@app.get("/")
@app.get("/kaithheathcheck")   
@app.get("/kaithhealthcheck")
@app.get("/health")
async def healthcheck():
    return {"status": "Agent is working",
            "agent": "fact-checker",
            "version": "1.0",
            "protocol": "JSON-RPC 2.0"
            }

@app.post("/a2a/factchecker")
async def fact_checker_route(request: JsonRpcRequest):
    try:
        user_messages = request.params.message

        claim = ""
        for part in user_messages.parts:
            if part.kind == "text" and part.text:
                claim += part.text + " "
            
        claim = claim.strip()
            
        if not claim:
            return JSONResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": "No text content found in message"
                }
            )

        greetings = ["hi", "hello", "hey", "help", "what can you do", "what do you do", "you do", "your purpose", "your task"]
        if claim.lower().strip() in greetings:
            help_text = """**Hello! I'm a Fact Checker AI.**
            I can help you verify claims and statements. Just send me any claim you want me to check!

            **Examples:**
            - "The Earth is flat"
            - "Coffee is bad for your health"
            - "Python is the most popular programming language"
            - Or any other claim

            Send me any claim to check!"""
            
            response_message = A2AMessage(
                role="assistant",
                parts=[MessagePart(kind="text", text=help_text)],
                # messageId=str(uuid4()), 
                # taskId=request.params.message.taskId  
            )
        
            artifact = Artifact(
                artifactId = str(uuid4()),
                name =  "factCheckerAgentResponse",
                parts = [MessagePart(kind="text", text=help_text)]
            )

            return JsonRpcResponse(
                id=request.id,
                result=ResponseMessage(
                    id=str(uuid4()),
                    status=ResponseStatus(state="completed"),
                    message=response_message,
                    artifacts=[artifact],
                    history=[request.params.message, response_message]
                )
            )
        
        result = await fact_checker.check_fact(claim)


        response_message = A2AMessage(
                role="assistant",
                parts=[MessagePart(kind="text", text=result)]
            )
        artifact = Artifact(
                artifactId = str(uuid4()),
                name =  "factCheckerAgentResponse",
                parts = [MessagePart(kind="text", text=result)]
                )

        return JsonRpcResponse(
            id=request.id,
            result=ResponseMessage(
                id=str(uuid4()),
                status=ResponseStatus(state="completed"),
                message=response_message,
                artifacts=[artifact],
                history=[request.params.message, response_message]
                )
            )
    except Exception as e:
        return JsonRpcError(
            id=request.id if hasattr(request, 'id') else "unknown",
            error={
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        )

