from typing import List
from pydantic import BaseModel, Field


class ReasoningStep(BaseModel):
    step: str = Field(..., description="Single reasoning step explanation.")


class ResponseModel(BaseModel):
    message: str = Field(..., description="The main textual content of the agent's reply, formatted and ready to be displayed to the user in the chat.")
    images: List[str] = Field(default=[], description="A list of local file paths for the exercise images to be sent along with the message. These paths are returned by the agent's tool. You MUST NOT create paths by yourself, you must use paths returned by the tool. The list can be empty if no images are needed for this reply.")
    reasoning_steps: List[ReasoningStep] = Field(default=[], description="List of reasoning steps, each as a dictionary with a 'step' field.")
