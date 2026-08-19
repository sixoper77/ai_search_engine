from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    async def get_query(q: str):
        pass

    @abstractmethod
    async def astream(q: str):
        pass
