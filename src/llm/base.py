import instructor
from dotenv import load_dotenv
from litellm import acompletion

from config import settings

from .absllm import BaseLLM
from .enums import Prompts
from .schemas import QueriesSchema

load_dotenv()

_, model = settings.get_model_and_key()
print(model)


class EveryLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model
        if "ollama" in model or "groq" in model:
            mode = instructor.Mode.MD_JSON
        else:
            mode = instructor.Mode.TOOLS_STRICT

        self.client = instructor.from_litellm(acompletion, mode=mode)

    async def get_query(self, q: str) -> QueriesSchema:
        response = await self.client.completions.create(
            model=self.model,
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
            response_model=QueriesSchema,
        )
        return response

    async def astream(self, q: str):
        response = await self.client.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": Prompts.PROMPT_ANSWER,
                },
                {
                    "role": "user",
                    "content": q,
                },
            ],
            stream=True,
        )
        async for chunk in response:
            yield chunk.choices[0].delta.content or ""


llm = EveryLLM(model)
