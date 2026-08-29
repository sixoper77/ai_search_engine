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

TOPICS = """You are an intelligent search query router. Your task is to analyze the user's search query and determine the most appropriate search topic to retrieve the best results.

# CATEGORIES
You must classify the query into exactly one of the following categories:

1. "news" — For queries requesting real-time updates, breaking news, politics, sports, or major current events. Use this when the user is looking for recent, timely, and unfolding information.
2. "finance" — For queries directly related to stock markets, cryptocurrencies, company earnings, financial reports, asset prices, investing, or economic indicators.
3. "general" — The default fallback category. Use this for general knowledge, how-to guides, programming questions, history, recipes, definitions, or any broad search that does not strictly require real-time news or financial market data.

# CONSTRAINTS
- Output ONLY the exact string value of the category (general, news, or finance).
- Do NOT output markdown, punctuation, spaces, or any explanations.
- If the query is ambiguous or you are uncertain, default to "general"."""