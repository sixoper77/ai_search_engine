from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Sequence

from src.search.schemas import BaseSource

from .enums import Prompts
from .schemas import AskSchema


class BaseLLM(ABC):
    @abstractmethod
    async def get_query[T: AskSchema](
        self, q: str, prompt: Prompts = Prompts.PROMPT_QUERY, *, schema: type[T]
    ) -> T:
        pass

    @abstractmethod
    def astream(self, q: str, data: Sequence[BaseSource]) -> AsyncGenerator[str, None]:
        pass
