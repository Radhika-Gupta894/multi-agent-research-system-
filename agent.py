from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import web_search, scrape_url
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API") or os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

llm = ChatGoogleGenerativeAI(
    model=model_name,
    api_key=gemini_key,
    max_retries=5,
)
#first agent 
def build_search_agent():
    return create_agent (
        model = llm,
        tools = [web_search],

    )

# second agent 
def build_reader_Agent():
    return create_agent(
        model = llm,
        tools = [scrape_url],
    )

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are a precise technical writer"),
    ("human", """Write a detailed research report on the topic below.
Topic: {topic}

Research Gathered:
{research}
Structure the report as:

1. Title
2. Introduction
3. Main findings (Bulleted)
4. Key References

Final Report: """)
])
writer_chain = (writer_prompt | llm | StrOutputParser()).with_retry(stop_after_attempt=5)

#critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the reseatch report below and evaluate it strictly. Focus on accuracy, clarity, and gaps in reasoning.
    
    Report:
    {report}
    REspond in this exact format:
    Score :X/10
    Strengths:
    -....
    -....

    Areas to Improve:
    -....
    -....

    One line verdict:
    ..."""),
])



critic_chain = (critic_prompt | llm | StrOutputParser()).with_retry(stop_after_attempt=5)

