QUERY_PROMPT = """You're an expert at creating search queries. Create the best search query in the user's language."""

QUERY_URL = """List of search queries.
        
        Generation rules:
        1. Assess the number of unique questions or topics in the message.
        2. Generate from 1 to N queries, where N equals the number of sub-questions (maximum of 5-7 queries).
        3. If the request is simple and contains a single idea, generate 1-2 queries.
        4. Each query must be self-contained and precise."""

QUERY_PHOTO = """Optimal query for search photos for user question"""

ANSWER = """You must give a clear and constructive answer to the user based on the information given to you, based on this given information, which completely covers the user's question."""

LANG_LOCALES = """Determine the language of the user query and return the exact locale code from the list. If the language is not recognized, return 'en-US'."""