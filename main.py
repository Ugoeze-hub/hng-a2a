from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from schemas import A2AMessage, A2ARequest, A2AResponse, FactCheckResult
from fact_checker_agent import FactCheckerAgent

load_dotenv()

app = FastAPI(title="Fact Checker Agent")

fact_checker = FactCheckerAgent()

@app.get("/")
async def healthcheck():
    return {"status": "Agent is working",
            "agent": "fact-checker",
            "version": "1.0"}

@app.post("/a2a/agent/factchecker")
async def fact_checker_route(request: A2ARequest):
    try:
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        
        if not user_messages:
            return JSONResponse(
                status_code = 400,
                content={"error": "No User message found"}
            )
        claim = user_messages[-1].content

        greetings = ["hi", "hello", "hey", "help", "what can you do"]
        if claim.lower().strip() in greetings:
            help_text = """Hello! I'm a Fact Checker AI.
            I can help you verify claims and statements. Just send me any claim you want me to check!

            Examples:
            - "The Earth is flat"
            - "Coffee is bad for your health"
            - "Python is the most popular programming language"

            I'll search for reliable sources and give you a verdict with explanation."""
        
            return A2AResponse(
                role="assistant",
                content=help_text
            )
        
        result = await fact_checker.check_fact(claim)
        
        return A2AResponse(
            role="assistant",
            content=result
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)