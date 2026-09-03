from pydantic import BaseModel, ConfigDict


class SearchSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    query: str | None = None
    max_results: int | None = None
    topic: str | None = None


class SerperSearchSchema(SearchSchema):
    queries: list[str]
    photo_query: str
    type: str
    country: str
    language: str


class SearxngSearchSchema(SearchSchema):
    search_links: list[str]
    search_photos: str
    language: str
