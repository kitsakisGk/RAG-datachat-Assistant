"""
Prompt templates for different RAG tasks
"""

# System prompts
SYSTEM_PROMPTS = {
    "general_qa": """You are a helpful AI assistant for data analysis.
You have access to relevant context from documents and databases.
Answer questions accurately based on the provided context.
If you cannot answer based on the context, say so clearly.""",

    "sql_generation": """You are an expert SQL query generator.
Given a database schema and a natural language question, generate a valid SQL query.
Only generate SELECT queries (read-only).
Ensure the query is safe and optimized.""",

    "data_analysis": """You are a data analyst AI assistant.
Analyze the provided data and generate insights.
Be specific with numbers and trends.
Explain your findings clearly.""",

    "document_qa": """You are a document analysis assistant.
Answer questions based strictly on the provided document context.
Quote relevant parts of the document when possible.
If the answer is not in the documents, say "I cannot find this information in the provided documents."
"""
}


# RAG QA Template
RAG_QA_TEMPLATE = """Context information is below:
---------------------
{context}
---------------------

Given the context information above, please answer the following question.
If the context doesn't contain enough information to answer, say so clearly.

Question: {question}

Answer:"""


# SQL Generation Template
SQL_GENERATION_TEMPLATE = """You are an expert SQL query generator.

Database Schema:
{schema}

Previous similar queries (for reference):
{examples}

User Question: {question}

Generate a valid SQL query to answer this question.
Requirements:
- Use only SELECT statements (read-only)
- Follow the exact table and column names from the schema
- Optimize for performance
- Handle NULL values appropriately
- Add comments to explain complex logic

SQL Query:"""


# Data Analysis Template
DATA_ANALYSIS_TEMPLATE = """You are analyzing the following data:

{data}

Question: {question}

Please provide:
1. Direct answer to the question
2. Key insights from the data
3. Any notable patterns or anomalies
4. Relevant statistics

Analysis:"""


# Document Summary Template
DOCUMENT_SUMMARY_TEMPLATE = """Please provide a comprehensive summary of the following document:

{document}

Include:
- Main topics and themes
- Key points and findings
- Important details
- Overall context

Summary:"""


# Conversation Template
CONVERSATION_TEMPLATE = """Previous conversation:
{history}

Retrieved context:
{context}

User: {question}"""
