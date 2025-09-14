"""
Scheduler Tasks - Define tasks for schedule extraction and processing
"""

from crewai import Task

def extract_schedule_task(agent, specialist_name, pdf_path):
    """Task to extract schedule for a specific specialist"""
    return Task(
        description=f"""
        Extract the complete schedule for specialist '{specialist_name}' from the PDF.
        
        Steps:
        1. Extract all text content from the PDF at {pdf_path}
        2. Locate the section for {specialist_name}
        3. Parse all appointments for this specialist including:
           - Date of appointment
           - Time of appointment
           - Client name
           - Session type (1 on 1 or Group)
        4. Format the schedule clearly with all sessions listed
        5. Sort sessions chronologically
        
        Handle various PDF formats and layouts.
        Be thorough - don't miss any appointments.
        """,
        agent=agent,
        expected_output="Complete list of sessions for the specialist with dates, times, and client names"
    )

def weekly_schedule_task(agent, specialist_name, pdf_path, week_offset=0):
    """Task to extract schedule for a specific week"""
    return Task(
        description=f"""
        Extract the schedule for specialist '{specialist_name}' for the week 
        {week_offset} weeks from now (0 = current week, -1 = last week).
        
        Steps:
        1. Extract all text from the PDF at {pdf_path}
        2. Find all sessions for {specialist_name}
        3. Filter sessions for the specified week only
        4. Include all relevant details:
           - Day and date
           - Time
           - Client name
           - Session type
        5. Organize by day of the week
        6. Provide a summary (total sessions, breakdown by type)
        
        Ensure accurate date filtering for the correct week.
        """,
        agent=agent,
        expected_output="Weekly schedule with all sessions for the specified week"
    )

def multi_specialist_schedule_task(agent, pdf_path):
    """Task to extract schedules for all specialists"""
    return Task(
        description=f"""
        Extract schedules for ALL specialists found in the PDF.
        
        Steps:
        1. Extract all text from the PDF at {pdf_path}
        2. Identify all specialists mentioned (Dr., Ms., Mr., etc.)
        3. For each specialist, extract their complete schedule
        4. Organize the output by specialist
        5. Include session counts for each specialist
        6. Provide an overall summary
        
        Be comprehensive - capture all specialists and all their sessions.
        Handle various naming conventions and titles.
        """,
        agent=agent,
        expected_output="Complete schedules for all specialists organized by name"
    )

def schedule_conflict_check_task(agent, pdf_path):
    """Task to check for scheduling conflicts"""
    return Task(
        description=f"""
        Analyze the schedule in the PDF for any conflicts or issues.
        
        Steps:
        1. Extract all schedules from {pdf_path}
        2. Check for:
           - Double-booked time slots for any specialist
           - Back-to-back appointments with no break
           - Unusually long gaps in schedules
           - Sessions scheduled outside normal hours
        3. Identify any clients with multiple appointments
        4. Flag any formatting issues or unclear entries
        5. Provide recommendations for optimization
        
        Be thorough in identifying potential issues.
        """,
        agent=agent,
        expected_output="Analysis report with any conflicts, issues, and recommendations"
    )

def client_appointments_task(agent, client_name, pdf_path):
    """Task to find all appointments for a specific client"""
    return Task(
        description=f"""
        Find all appointments for client '{client_name}' across all specialists.
        
        Steps:
        1. Extract all text from the PDF at {pdf_path}
        2. Search for all mentions of '{client_name}'
        3. Extract appointment details:
           - Date and time
           - Specialist name
           - Session type
        4. Sort appointments chronologically
        5. Identify any patterns (regular weekly sessions, etc.)
        6. Note if client has sessions with multiple specialists
        
        Use case-insensitive matching for the client name.
        Be thorough - check all sections of the PDF.
        """,
        agent=agent,
        expected_output="Complete list of all appointments for the specified client"
    )
