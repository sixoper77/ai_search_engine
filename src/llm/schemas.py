from typing import Annotated

from pydantic import BaseModel, Field

from .enums import Prompts


class QueriesSchema(BaseModel):
    search_links: Annotated[str, Field(description=Prompts.PROMPT_URL)]
    search_photos: Annotated[str, Field(description=Prompts.PROMPT_PHOTO)]



