"""
Scheduler Agent - Extracts and processes schedule information from PDFs
"""

from crewai import Agent
from tools.pdf_tools import PDFExtractor, ScheduleParser
from config import get_llm
import os

def scheduler_agent(schedule_pdf=None):
    # Use provided PDF or default to sample
    if schedule_pdf is None:
        schedule_pdf = "data/sample_schedule.pdf"

    # Check if PDF exists
    pdf_exists = os.path.exists(schedule_pdf) if schedule_pdf else False

    backstory = f"""You are a meticulous scheduler who specializes in
        reading and interpreting schedule documents. You can extract
        specific specialist schedules from complex PDFs, identify client
        appointments, and organize time slots efficiently. You have a keen
        eye for detail and never miss an appointment.

        Current schedule PDF: {schedule_pdf if pdf_exists else 'No PDF file available'}

        IMPORTANT: When using the PDF Extractor tool, use the path: {schedule_pdf}
        If the PDF doesn't exist, report that no schedule is available."""

    return Agent(
        role='Schedule Coordinator',
        goal='Extract and organize appointment schedules from PDF documents',
        backstory=backstory,
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
