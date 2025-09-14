"""
CRM Agent - Handles client data management using markdown files
"""

from crewai import Agent
from tools.markdown_tools import (
    MarkdownReader,
    MarkdownWriter,
    ClientParser
)
from config import get_llm

def crm_agent():
    return Agent(
        role='CRM Manager',
        goal='Manage client information efficiently and accurately',
        backstory="""You are an experienced CRM specialist who excels at
        organizing client data. You can handle inconsistent data formats,
        extract relevant information, and maintain a clean client database.
        You're particularly skilled at parsing markdown files and understanding
        various data input formats.""",
        tools=[
            MarkdownReader(),
            MarkdownWriter(),
            ClientParser()
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True
    )
