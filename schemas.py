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

class A2AMessage(BaseModel):
    kind: Literal["message"] = "message"
    role: str
    parts: List[MessagePart]
    messageId: Optional[str] = None #str = Field(default_factory=lambda: str(uuid4()))
    taskId:  Optional[str] = None #str = Field(default_factory=lambda: str(uuid4()))
    #metadata: Optional[Dict[str, Any]] = None

class MessageConfiguration(BaseModel):
    blocking: bool = True
    acceptedOutputModes: List[str] = ["text/plain", "text/markdown"]

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

class Artifact(BaseModel):
    artifactId: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    parts: List[MessagePart]

class ResponseMessage(BaseModel):
    id : str
    contextId: Optional[str] = None #str = Field(default_factory=lambda: str(uuid4()))
    status: ResponseStatus
    message: A2AMessage
    artifacts: List[Artifact] = []
    history: List[A2AMessage] = []
    kind: Literal["task"] = "task"


class JsonRpcResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str
    result: Optional[ResponseMessage] = None

class JsonRpcError(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str
    error: Optional[Dict[str, Any]] = None

