from enum import StrEnum

from .prompts import *


class Prompts(StrEnum):
    PROMPT_QUERY = QUERY_PROMPT
    PROMPT_PHOTO = QUERY_PHOTO
    PROMPT_URL = QUERY_URL
    PROMPT_ANSWER = ANSWER
