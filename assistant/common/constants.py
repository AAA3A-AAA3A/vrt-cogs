MODELS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-16k-0301": 16384,
    "gpt-3.5-turbo-16k-0613": 16384,
    "gpt-4": 8192,
    "gpt-4-0301": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0301": 32768,
    "gpt-4-32k-0613": 32768,
    "code-davinci-002": 8001,
    "text-davinci-003": 4097,
    "text-davinci-002": 4097,
    "text-curie-001": 2049,
    "text-babbage-001": 2049,
    "text-ada-001": 2049,
    "text-embedding-ada-002": 8191,
    "text-embedding-ada-002-v2": 8191,
}
PRICES = {
    "gpt-3.5-turbo": [0.0015, 0.002],
    "gpt-3.5-turbo-0301": [0.0015, 0.002],
    "gpt-3.5-turbo-0613": [0.0015, 0.002],
    "gpt-3.5-turbo-16k": [0.003, 0.004],
    "gpt-3.5-turbo-16k-0613": [0.003, 0.004],
    "gpt-4": [0.03, 0.06],
    "gpt-4-0301": [0.03, 0.06],
    "gpt-4-0613": [0.03, 0.06],
    "gpt-4-32k": [0.06, 0.12],
    "gpt-4-32k-0301": [0.06, 0.12],
    "gpt-4-32k-0613": [0.06, 0.12],
    "text-ada-001": [0.0004, 0.0016],
    "text-babbage-001": [0.0006, 0.0024],
    "text-curie-001": [0.003, 0.012],
    "text-davinci-002": [0.03, 0.12],
    "text-davinci-003": [0.03, 0.12],
    "code-davinci-002": [0.03, 0.12],
    "text-embedding-ada-002": [0.0001, 0.0001],
    "text-embedding-ada-002-v2": [0.0001, 0.0001],
}
SUPPORTS_FUNCTIONS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
]
CHAT = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0301",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0301",
    "gpt-4-32k-0613",
    "code-davinci-002",
]
COMPLETION = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]
READ_EXTENSIONS = [
    ".txt",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".xml",
    ".html",
    ".ini",
    ".css",
    ".toml",
    ".md",
    ".ini",
    ".conf",
    ".go",
    ".cfg",
    ".java",
    ".c",
    ".php",
    ".swift",
    ".vb",
    ".xhtml",
    ".rss",
    ".css",
    ".asp",
    ".js",
    ".ts",
    ".cs",
    ".c++",
    ".cc",
    ".ps1",
    ".bat",
    ".batch",
    ".shell",
    ".env",
]
REACT_SUMMARY_MESSAGE = """
Your job is to summarize text to use as embeddings. Respond only with the summary of the text.
"""
REACT_NAME_MESSAGE = """
Your job is to read a snippet of text and come up with a short descriptive name for it. Only respond with the name of the summary.
"""
CREATE_EMBEDDING = {
    "name": "create_embedding",
    "description": "Use this function to save information about something outside of the context of the current conversation, and can be referenced later. useful when someone corrects you or tells you something new.",
    "parameters": {
        "type": "object",
        "properties": {
            "embedding_name": {
                "type": "string",
                "description": "A short unique name for the embedding entry, this should be a descriptive name and contain less than 100 characters, or less than 4 separate words.",
            },
            "embedding_text": {
                "type": "string",
                "description": "Detailed summary of information to be stored based on the context of the conversation or correction. Write it as if you are the one telling someone the information.",
            },
        },
        "required": ["embedding_name", "embedding_text"],
    },
}
SEARCH_EMBEDDINGS = {
    "name": "search_embeddings",
    "description": "Use this function to search embeddings for related info",
    "parameters": {
        "type": "object",
        "properties": {
            "search_query": {
                "type": "string",
                "description": "The context you wish to search for",
            }
        },
        "required": ["search_query"],
    },
}
