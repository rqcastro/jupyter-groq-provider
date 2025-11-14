# groq_provider.py
from typing import ClassVar, List, Optional, Any

import os
import requests

from jupyter_ai_magics import BaseProvider
from jupyter_ai_magics.providers import EnvAuthStrategy, Field, TextField

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqChatModel(BaseChatModel):
    """
    Custom ChatModel that calls the Groq API directly (OpenAI style).
    Does not depend on langchain-groq.
    """

    model: str
    api_key: str
    max_tokens: int = 4096
    temperature: float = 1.0

    @property
    def _llm_type(self) -> str:
        # Internal identifier – can be any string
        return "groq-chat"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
       
        # Convert LangChain messages -> OpenAI-like format
        openai_messages = []
        for m in messages:
            role = "user"
            if m.type == "system":
                role = "system"
            elif m.type == "ai":
                role = "assistant"
            # For simplicity, we assume content is a string
            openai_messages.append({"role": role, "content": m.content})

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        if stop is not None:
            payload["stop"] = stop

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(GROQ_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        content = data["choices"][0]["message"]["content"]

        ai_msg = AIMessage(content=content)
        generation = ChatGeneration(message=ai_msg)
        return ChatResult(generations=[generation])


class GroqProvider(BaseProvider, GroqChatModel):
    """
    Provider for Jupyter AI, using the GroqChatModel above.
    """

    id = "groq"
    name = "Groq"
    model_id_key = "model"

    # Models that will appear in the dropdown / config
    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "deepseek-r1-distill-llama-70b",
    ]

    # Get the API key from env var GROQ_API_KEY and pass as api_key
    auth_strategy = EnvAuthStrategy(
        name="GROQ_API_KEY",
        keyword_param="api_key",
    )

    # Extra configurable fields in the UI
    fields: ClassVar[List[Field]] = [
        TextField(
            key="temperature",
            label="Temperature (0.0 - 2.0)",
            format="text",
        ),
        TextField(
            key="max_tokens",
            label="Max tokens",
            format="text",
        ),
    ]

    def __init__(self, **kwargs: Any):
       
       # Ensure there is always a model_id
        if "model_id" not in kwargs or not kwargs["model_id"]:
            # use the first from the list as default
            kwargs["model_id"] = type(self).models[0]
        
       # Defaults similar to your standalone code
        kwargs.setdefault("max_tokens", 4096)
        kwargs.setdefault("temperature", 1.1)

        super().__init__(**kwargs)
