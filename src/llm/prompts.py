QUERY_PROMPT = """You're an expert at creating search queries. Create the best search query in the user's language."""

QUERY_URL = """List of search queries.
        
        Generation rules:
        1. Assess the number of unique questions or topics in the message.
        2. Generate from 1 to N queries, where N equals the number of sub-questions (maximum of 5-7 queries).
        3. If the request is simple and contains a single idea, generate 1-2 queries.
        4. Each query must be self-contained and precise."""

QUERY_PHOTO = """Optimal query for search photos for user question"""

ANSWER = """You must give a clear and constructive answer to the user based on the information given to you, based on this given information, which completely covers the user's question.In the end of your answer,add urls and titel for each url which I sent you"""

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


TYPES_SERPER = """You are an intelligent search routing assistant. Your task is to analyze the user's query and determine the most appropriate search type from the following exact values: "search", "reviews", "news", "shopping", "scholar", "patents".

Rules for classification:
- "scholar": Use for academic research, scientific papers, peer-reviewed articles, dissertations, and university publications.
- "patents": Use for queries specifically searching for registered patents, inventions, technical blueprints, and intellectual property.
- "shopping": Use when the user expresses an intent to purchase products, compare prices, or find online stores.
- "reviews": Use when the user is explicitly looking for opinions, feedback, or ratings on products, businesses, or services.
- "news": Use for current events, recent developments, journalism, or breaking news.
- "search": Use as the default fallback for general web queries, factual questions, tutorials, or anything that does not strictly fit into the above categories.

Output ONLY the exact string of the selected category. Do not include quotes, punctuation, explanations, or any additional text."""

GET_FACTS = """ You are a highly precise information extraction system. Your task is to extract factual statements from the provided text snippets that directly answer the target question.**Extraction Rules & Constraints:**
1. **Direct Relevance:** Extract ONLY facts that directly and explicitly answer the target question. Ignore all irrelevant or tangential information.
2. **Strict Grounding (No Hallucinations):** Base your extraction strictly on the provided snippets. Do not infer, deduce, summarize beyond recognition, or use outside knowledge. 
3. **Format & Conciseness:** Present each extracted fact as a single, short, and clear sentence. Do not combine multiple distinct facts into complex sentences.
5. **Output Structure:** Output a simple bulleted list. Do not add conversational filler, introductions, or conclusions."""

FACT_FIELD = """A single, concise factual sentence directly answering the query. Strictly based on the text, no inferences."""
URL_FIELD = """The exact source snippet number or URL where this fact was found."""

EXPLANATION = """A short explanation of what specific information is missing (if False) or why it is complete (if True)."""


REFLECTION = """You are a strict evaluation system for a QA pipeline. Your task is to determine whether the provided "Extracted Facts" contain sufficient information to completely and accurately answer the "User Query".

**Evaluation Rules:**
1. **Strict Sufficiency:** The facts must provide a FULL and direct answer to the query. If the facts only partially answer the question, or if crucial details are missing, you must evaluate them as insufficient.
2. **No Outside Knowledge:** You are strictly forbidden from using your internal training data to fill in gaps. Base your decision entirely on the provided facts.
3. **No Assumptions:** If the query asks for a specific metric, date, or name, and the facts only hint at it without stating it explicitly, the facts are insufficient.
"""
QUERIES = """ If 'is_sufficient' is False, generate 1-3 highly targeted search queries to find the strictly missing information. Queries must be optimized for a search engine. Leave empty if 'is_sufficient' is True."""

CHAT_NAME = (
    """Short chat title (max 20 letters), in the same language as the user's question"""
)
