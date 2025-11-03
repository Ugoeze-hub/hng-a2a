from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from uuid import uuid4
from datetime import datetime, timezone

class MessagePart(BaseModel):
    kind: Literal["text", "image", "file", "data"]
    text: Optional[str] = None
    data: Optional[ Any] = None
    url: Optional[str] = None
    file_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None  

class A2AMessage(BaseModel):
    kind: Literal["message"] = "message"
    role: str
    parts: List[MessagePart]
    messageId: Optional[str] = None 
    taskId:  Optional[str] = None 

class MessageConfiguration(BaseModel):
    blocking: bool = True

class MessageParams(BaseModel):
    message: A2AMessage
    configuration: Optional[MessageConfiguration] = Field(default_factory=MessageConfiguration)

class JsonRpcRequest(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str
    method: str
    params: MessageParams

class ResponseStatus(BaseModel):
    state: Literal["completed", "failed", "working"]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    message: A2AMessage

class Artifact(BaseModel):
    artifactId: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    parts: List[MessagePart]

class ResponseMessage(BaseModel):
    kind: Literal["task"] = "task"
    id : str
    contextId: Optional[str] = None 
    status: ResponseStatus
    artifacts: List[Artifact] = []
    history: List[A2AMessage] = []
    


class JsonRpcResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str
    result: Optional[ResponseMessage] = None
    error: Optional[Dict[str, Any]] = None

class JsonRpcError(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str
    result: Optional[ResponseMessage] = None
    error: Optional[Dict[str, Any]]
    

