from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from .schemas import AskSchema


class BaseLLM(ABC):
    @abstractmethod
    async def get_query[T: AskSchema](self, q: str, schema: type[T]) -> T:
        pass

    @abstractmethod
    def astream(self, q: str, data: list) -> AsyncGenerator[str, None]:
        pass
