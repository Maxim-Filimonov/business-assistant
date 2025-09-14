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

    # Sample schedule data organized by days
    week_schedule = {
        "Monday": {
            "date": monday.strftime('%m/%d/%Y'),
            "appointments": [
                ("9:00 AM", "Dr. Johnson", "Sarah Williams", "1 on 1 session"),
                ("10:00 AM", "Dr. Johnson", "Mike Chen", "1 on 1 session"),
                ("10:00 AM", "Ms. Thompson", "Susan Park", "1 on 1 session"),
                ("11:00 AM", "Dr. Johnson", "Group Therapy", "Group session"),
                ("11:00 AM", "Ms. Thompson", "Michael Brown", "1 on 1 session"),
                ("1:00 PM", "Ms. Thompson", "Group Therapy", "Group session"),
                ("2:00 PM", "Dr. Johnson", "Emily Davis", "1 on 1 session"),
                ("3:00 PM", "Ms. Thompson", "Ashley Jones", "1 on 1 session"),
            ]
        },
        "Tuesday": {
            "date": (monday + timedelta(days=1)).strftime('%m/%d/%Y'),
            "appointments": [
                ("9:00 AM", "Dr. Smith", "Alex Johnson", "1 on 1 session"),
                ("10:00 AM", "Dr. Smith", "Maria Garcia", "1 on 1 session"),
                ("11:00 AM", "Dr. Smith", "David Wilson", "1 on 1 session"),
                ("2:00 PM", "Dr. Smith", "Group Therapy", "Group session"),
            ]
        },
        "Wednesday": {
            "date": (monday + timedelta(days=2)).strftime('%m/%d/%Y'),
            "appointments": [
                ("9:00 AM", "Dr. Johnson", "John Smith", "1 on 1 session"),
                ("9:00 AM", "Ms. Thompson", "Tom Anderson", "1 on 1 session"),
                ("10:00 AM", "Ms. Thompson", "Susan Park", "1 on 1 session"),
                ("10:30 AM", "Dr. Johnson", "Lisa Anderson", "1 on 1 session"),
                ("1:00 PM", "Dr. Johnson", "Group Therapy", "Group session"),
                ("2:00 PM", "Ms. Thompson", "Michael Brown", "1 on 1 session"),
                ("3:00 PM", "Dr. Johnson", "Robert Brown", "1 on 1 session"),
            ]
        },
        "Thursday": {
            "date": (monday + timedelta(days=3)).strftime('%m/%d/%Y'),
            "appointments": [
                ("10:00 AM", "Dr. Smith", "Jennifer Lee", "1 on 1 session"),
                ("11:00 AM", "Dr. Smith", "James Martinez", "1 on 1 session"),
                ("1:00 PM", "Dr. Smith", "Alex Johnson", "1 on 1 session"),
                ("3:00 PM", "Dr. Smith", "Group Therapy", "Group session"),
            ]
        },
        "Friday": {
            "date": (monday + timedelta(days=4)).strftime('%m/%d/%Y'),
            "appointments": [
                ("9:00 AM", "Dr. Johnson", "Sarah Williams", "1 on 1 session"),
                ("10:00 AM", "Dr. Johnson", "Mike Chen", "1 on 1 session"),
                ("10:00 AM", "Ms. Thompson", "Group Therapy", "Group session"),
                ("1:00 PM", "Ms. Thompson", "Ashley Jones", "1 on 1 session"),
                ("2:00 PM", "Dr. Johnson", "Emily Davis", "1 on 1 session"),
                ("2:00 PM", "Ms. Thompson", "Tom Anderson", "1 on 1 session"),
            ]
        }
    }

    # Draw the schedule grouped by days
    y_position = height - 2*inch

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for day_name in days_order:
        day_info = week_schedule[day_name]

        # Day header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, y_position, f"{day_name} - {day_info['date']}")
        y_position -= 0.3*inch

        # Sort appointments by time for better readability
        sorted_appointments = sorted(day_info['appointments'],
                                    key=lambda x: (x[0].split()[0].zfill(2), x[0].split()[1]))

        # Draw appointments
        c.setFont("Helvetica", 10)
        for time, specialist, client, session_type in sorted_appointments:
            appointment_text = f"{time}: {specialist} - {client} ({session_type})"
            c.drawString(1.3*inch, y_position, appointment_text)
            y_position -= 0.18*inch

        y_position -= 0.2*inch

        # Check if we need a new page
        if y_position < 2*inch:
            c.showPage()
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, height - 1*inch, "Weekly Schedule (Continued)")
            y_position = height - 1.5*inch

    # Save the PDF
    c.save()

    print(f"✅ Sample schedule PDF created: {pdf_path}")
    print(f"📅 Schedule covers week of {monday.strftime('%m/%d/%Y')}")

    return pdf_path

if __name__ == "__main__":
    generate_sample_schedule()
