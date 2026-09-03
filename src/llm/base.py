from collections.abc import AsyncGenerator

import instructor
from dotenv import load_dotenv
from litellm import acompletion

from config import settings

from .absllm import BaseLLM
from .enums import Prompts
from .schemas import AskSchema

load_dotenv()

model_url, model = settings.get_model_and_key()
print(model_url, model)


class EveryLLM(BaseLLM):
    def __init__(self, model: str, api_base: str | None = None):
        self.model = model
        self.api_base = api_base
        if "ollama" in model or "groq" in model:
            mode = instructor.Mode.MD_JSON
        else:
            mode = instructor.Mode.TOOLS_STRICT

        self.client = instructor.from_litellm(acompletion, mode=mode)

    async def get_query[T: AskSchema](self, q: str, schema: type[T]) -> T:
        response = await self.client.completions.create(  # type: ignore
            model=self.model,
            api_base=self.api_base,
            messages=[
                {
                    "role": "system",
                    "content": Prompts.PROMPT_QUERY,
                },
                {
                    "role": "user",
                    "content": q,
                },
            ],
            response_model=schema,
        )
        return response

    async def astream(self, q: str, data: list) -> AsyncGenerator[str, None]: 
        data_for_ai = "\n---\n".join(data)
        combined_prompt = f"\n Data:\n{data_for_ai}\nUser Question:\n{q}"
        response = await acompletion(
            model=self.model,
            api_base=self.api_base,
            messages=[
                {
                    "role": "system",
                    "content": Prompts.PROMPT_ANSWER,
                },
                {
                    "role": "user",
                    "content": combined_prompt,
                },
            ],
            stream=True,
        )

        async for chunk in response:
            token = chunk.choices[0].delta.content
            if token is not None:
                yield token
                


llm = EveryLLM(model, model_url)
