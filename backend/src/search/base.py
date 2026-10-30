from abc import ABC, abstractmethod

from src.search.schemas import SearchSchema


class BaseSearch[T_SearchData: SearchSchema, T_ResponseData](ABC):
    @abstractmethod
    async def search(self, data: T_SearchData) -> T_ResponseData:
        pass
