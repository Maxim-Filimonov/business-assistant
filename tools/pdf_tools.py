"""
PDF Tools for Schedule Extraction
"""

from crewai.tools import BaseTool
import PyPDF2
import pdfplumber
import re
from typing import List, Dict
from datetime import datetime, timedelta

class PDFExtractor(BaseTool):
    name: str = "PDF Extractor"
    description: str = "Extracts text content from PDF files"

    def _run(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            if not text.strip():
                # Fallback to PyPDF2 if pdfplumber fails
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"

            return text
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"

class ScheduleParser(BaseTool):
    name: str = "Schedule Parser"
    description: str = "Parses schedule information for specific specialists"

    def _run(self, pdf_text: str, specialist_name: str) -> List[Dict]:
        """Parse schedule for a specific specialist"""
        sessions = []
        lines = pdf_text.split('\n')

        # Common time patterns
        time_pattern = r'(\d{1,2}[:]\d{2}\s*[APap][Mm])'
        date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'

        specialist_section = False
        current_date = None

        for i, line in enumerate(lines):
            # Check if we're in the specialist's section
            if specialist_name.lower() in line.lower():
                specialist_section = True
                continue

            # Check for section change (another specialist name)
            if specialist_section and any(title in line for title in ['Dr.', 'Ms.', 'Mr.', 'Mrs.']):
                if specialist_name.lower() not in line.lower():
                    specialist_section = False
                    continue

            if specialist_section:
                # Extract date
                date_match = re.search(date_pattern, line)
                if date_match:
                    current_date = date_match.group(1)

                # Extract time and client
                time_match = re.search(time_pattern, line)
                if time_match and current_date:
                    time = time_match.group(1)

                    # Extract client name (usually after time)
                    remaining = line[time_match.end():].strip()

                    # Remove common separators
                    remaining = re.sub(r'^[-:,]\s*', '', remaining)

                    # Extract client name (before any session type indicator)
                    client_match = re.match(r'([A-Za-z\s]+)', remaining)
                    if client_match:
                        client_name = client_match.group(1).strip()

                        # Determine session type
                        session_type = "1 on 1 session"  # default
                        if 'group' in line.lower():
                            session_type = "Group session"

                        session = {
                            'date': current_date,
                            'time': time,
                            'client': client_name,
                            'specialist': specialist_name,
                            'type': session_type
                        }
                        sessions.append(session)

        return sessions

class WeekFilter(BaseTool):
    name: str = "Week Filter"
    description: str = "Filters sessions for a specific week"

    def _run(self, sessions: List[Dict], week_offset: int = 1) -> List[Dict]:
        """Filter sessions for a specific week (offset from current week)"""
        today = datetime.now()

        # Calculate the target week's start and end
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)
        target_week_start = current_week_start - timedelta(weeks=week_offset)
        target_week_end = target_week_start + timedelta(days=6)

        filtered_sessions = []

        for session in sessions:
            try:
                # Parse session date (handle various formats)
                date_str = session['date']

                # Try different date formats
                date_formats = [
                    '%m/%d/%Y',
                    '%m-%d-%Y',
                    '%d/%m/%Y',
                    '%d-%m-%Y',
                    '%m/%d/%y',
                    '%m-%d-%y'
                ]

                session_date = None
                for fmt in date_formats:
                    try:
                        session_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue

                if session_date:
                    # Check if session is in target week
                    if target_week_start <= session_date <= target_week_end:
                        filtered_sessions.append(session)

            except Exception as e:
                print(f"Error parsing date {session.get('date')}: {e}")
                continue

        return filtered_sessions
