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

        IMPORTANT INSTRUCTIONS:
        1. Use the Markdown Reader tool ONLY ONCE to read the file at: {clients_file}
        2. After reading the file, use the Client Parser tool to parse the content
        3. Do NOT repeatedly read the same file - read it once and work with the data
        4. If the file is empty or has incomplete data, report what's available
        5. You have a maximum of 3 iterations to complete your task""",
        tools=[
            MarkdownReader(),
            SafeMarkdownWriter(),
            ClientParser()
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True,
        max_execution_time=30  # Add timeout to prevent infinite loops
    )
