#!/usr/bin/env python
"""
Generate a sample schedule PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import os

def generate_sample_schedule():
    """Generate a sample schedule PDF"""

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    pdf_path = "data/sample_schedule.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Set up the document
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "Weekly Schedule - Mental Health Clinic")

    # Add date range
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)

    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.3*inch,
                f"Week of {monday.strftime('%m/%d/%Y')} - {friday.strftime('%m/%d/%Y')}")

    # Sample schedule data
    specialists = [
        {
            "name": "Dr. Johnson",
            "sessions": [
                {"day": "Monday", "date": monday.strftime('%m/%d/%Y'),
                 "appointments": [
                     ("9:00 AM", "Sarah Williams", "1 on 1 session"),
                     ("10:00 AM", "Mike Chen", "1 on 1 session"),
                     ("11:00 AM", "Group Therapy", "Group session"),
                     ("2:00 PM", "Emily Davis", "1 on 1 session"),
                 ]},
                {"day": "Wednesday", "date": (monday + timedelta(days=2)).strftime('%m/%d/%Y'),
                 "appointments": [
                     ("9:00 AM", "John Smith", "1 on 1 session"),
                     ("10:30 AM", "Lisa Anderson", "1 on 1 session"),
                     ("1:00 PM", "Group Therapy", "Group session"),
                     ("3:00 PM", "Robert Brown", "1 on 1 session"),
                 ]},
                {"day": "Friday", "date": (monday + timedelta(days=4)).strftime('%m/%d/%Y'),
                 "appointments": [
                     ("9:00 AM", "Sarah Williams", "1 on 1 session"),
                     ("10:00 AM", "Mike Chen", "1 on 1 session"),
                     ("2:00 PM", "Emily Davis", "1 on 1 session"),
                 ]}
            ]
        },
        {
            "name": "Dr. Smith",
            "sessions": [
                {"day": "Tuesday", "date": (monday + timedelta(days=1)).strftime('%m/%d/%Y'),
                 "appointments": [
                     ("9:00 AM", "Alex Johnson", "1 on 1 session"),
                     ("10:00 AM", "Maria Garcia", "1 on 1 session"),
                     ("11:00 AM", "David Wilson", "1 on 1 session"),
                     ("2:00 PM", "Group Therapy", "Group session"),
                 ]},
                {"day": "Thursday", "date": (monday + timedelta(days=3)).strftime('%m/%d/%Y'),
                 "appointments": [
                     ("10:00 AM", "Jennifer Lee", "1 on 1 session"),
                     ("11:00 AM", "James Martinez", "1 on 1 session"),
                     ("1:00 PM", "Alex Johnson", "1 on 1 session"),
                     ("3:00 PM", "Group Therapy", "Group session"),
                 ]}
            ]
        }
    ]

    # Draw the schedule
    y_position = height - 2*inch

    for specialist in specialists:
        # Specialist name
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, y_position, specialist["name"])
        y_position -= 0.3*inch

        for session_day in specialist["sessions"]:
            # Day and date
            c.setFont("Helvetica-Bold", 12)
            c.drawString(1.2*inch, y_position, f"{session_day['day']} - {session_day['date']}")
            y_position -= 0.2*inch

            # Appointments
            c.setFont("Helvetica", 10)
            for time, client, session_type in session_day["appointments"]:
                c.drawString(1.5*inch, y_position, f"{time}: {client} - {session_type}")
                y_position -= 0.15*inch

            y_position -= 0.1*inch

        y_position -= 0.3*inch

        # Check if we need a new page
        if y_position < 2*inch:
            c.showPage()
            y_position = height - 1*inch

    # Save the PDF
    c.save()

    print(f"✅ Sample schedule PDF created: {pdf_path}")
    print(f"📅 Schedule covers week of {monday.strftime('%m/%d/%Y')}")

    return pdf_path

if __name__ == "__main__":
    generate_sample_schedule()
