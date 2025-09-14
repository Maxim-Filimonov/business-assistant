"""
Invoice Agent - Generates invoices based on schedule and pricing
"""

from crewai import Agent
from tools.invoice_tools import (
    PricingReader,
    InvoiceGenerator,
    SessionCalculator
)
from config import get_llm

def invoice_agent():
    return Agent(
        role='Invoice Specialist',
        goal='Generate accurate invoices based on sessions and pricing',
        backstory="""You are a detail-oriented billing specialist who
        creates precise invoices. You understand different session types,
        apply correct pricing, calculate totals accurately, and format
        invoices professionally. You ensure all billable sessions from
        the past week are included and properly categorized.""",
        tools=[
            PricingReader(),
            InvoiceGenerator(),
            SessionCalculator()
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True
    )
