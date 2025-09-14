"""
CRM Agent - Handles client data management using markdown files
"""

from crewai import Agent
from tools.markdown_tools import (
    MarkdownReader,
    SafeMarkdownWriter,
    ClientParser
)
from config import get_llm

def crm_agent(clients_file="data/clients.md"):
    return Agent(
        role='CRM Manager',
        goal='Manage client information efficiently and accurately',
        backstory=f"""You are an experienced CRM specialist who excels at
        organizing client data. You can handle inconsistent data formats,
        extract relevant information, and maintain a clean client database.
        You're particularly skilled at parsing markdown files and understanding
        various data input formats.

        The client data is stored in a markdown file located at: {clients_file}
        You must use this file path when you need to read or write client data.""",
        tools=[
            MarkdownReader(),
            SafeMarkdownWriter(),
            ClientParser()
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True
    )
