"""
Scheduler Agent - Extracts and processes schedule information from PDFs
"""

from crewai import Agent
from tools.pdf_tools import PDFExtractor, ScheduleParser
from config import get_llm

def scheduler_agent():
    return Agent(
        role='Schedule Coordinator',
        goal='Extract and organize appointment schedules from PDF documents',
        backstory="""You are a meticulous scheduler who specializes in
        reading and interpreting schedule documents. You can extract
        specific specialist schedules from complex PDFs, identify client
        appointments, and organize time slots efficiently. You have a keen
        eye for detail and never miss an appointment.""",
        tools=[
            PDFExtractor(),
            ScheduleParser()
        ],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=True
    )
