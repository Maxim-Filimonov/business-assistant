"""CRM Agent - Handles client data management using a SQLite database."""

from crewai import Agent

from config import get_llm
from tools.crm_db_tools import (
    CRMClientApplyUpdate,
    CRMClientDiffPreview,
    CRMClientListMarkdownExporter,
    CRMClientReader,
)


def crm_agent(db_path: str = "data/clients.db"):
    return Agent(
        role="CRM Manager",
        goal="Manage client information efficiently and accurately",
        backstory=(
            "You are an experienced CRM specialist who keeps the official client "
            "records inside a local SQLite database. You can parse legacy "
            "markdown data, surface a diff preview for any change, and ensure "
            "approved updates are exported as readable markdown snapshots."
        ),
        tools=[
            CRMClientReader(db_path=db_path),
            CRMClientDiffPreview(db_path=db_path),
            CRMClientApplyUpdate(db_path=db_path),
            CRMClientListMarkdownExporter(db_path=db_path),
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True,
    )
