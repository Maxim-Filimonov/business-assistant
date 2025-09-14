#!/usr/bin/env python
"""
Create a text-based schedule file for testing (alternative to PDF)
"""

from datetime import datetime, timedelta
import os

def create_text_schedule():
    """Create a text schedule file that mimics PDF content"""

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    schedule_path = "data/schedule.txt"

    # Get current week dates
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    schedule_content = f"""WEEKLY SCHEDULE - MENTAL HEALTH CLINIC
Week of {monday.strftime('%m/%d/%Y')} - {(monday + timedelta(days=4)).strftime('%m/%d/%Y')}

================================================================================

Dr. Johnson
-----------

Monday - {monday.strftime('%m/%d/%Y')}
  9:00 AM: Sarah Williams - 1 on 1 session
  10:00 AM: Mike Chen - 1 on 1 session
  11:00 AM: Group Therapy - Group session
  2:00 PM: Emily Davis - 1 on 1 session

Wednesday - {(monday + timedelta(days=2)).strftime('%m/%d/%Y')}
  9:00 AM: John Smith - 1 on 1 session
  10:30 AM: Lisa Anderson - 1 on 1 session
  1:00 PM: Group Therapy - Group session
  3:00 PM: Robert Brown - 1 on 1 session

Friday - {(monday + timedelta(days=4)).strftime('%m/%d/%Y')}
  9:00 AM: Sarah Williams - 1 on 1 session
  10:00 AM: Mike Chen - 1 on 1 session
  2:00 PM: Emily Davis - 1 on 1 session

================================================================================

Dr. Smith
---------

Tuesday - {(monday + timedelta(days=1)).strftime('%m/%d/%Y')}
  9:00 AM: Alex Johnson - 1 on 1 session
  10:00 AM: Maria Garcia - 1 on 1 session
  11:00 AM: David Wilson - 1 on 1 session
  2:00 PM: Group Therapy - Group session

Thursday - {(monday + timedelta(days=3)).strftime('%m/%d/%Y')}
  10:00 AM: Jennifer Lee - 1 on 1 session
  11:00 AM: James Martinez - 1 on 1 session
  1:00 PM: Alex Johnson - 1 on 1 session
  3:00 PM: Group Therapy - Group session

================================================================================

Ms. Thompson
------------

Monday - {monday.strftime('%m/%d/%Y')}
  10:00 AM: Susan Park - 1 on 1 session
  11:00 AM: Michael Brown - 1 on 1 session
  1:00 PM: Group Therapy - Group session
  3:00 PM: Ashley Jones - 1 on 1 session

Wednesday - {(monday + timedelta(days=2)).strftime('%m/%d/%Y')}
  9:00 AM: Tom Anderson - 1 on 1 session
  10:00 AM: Susan Park - 1 on 1 session
  2:00 PM: Michael Brown - 1 on 1 session

Friday - {(monday + timedelta(days=4)).strftime('%m/%d/%Y')}
  10:00 AM: Group Therapy - Group session
  1:00 PM: Ashley Jones - 1 on 1 session
  2:00 PM: Tom Anderson - 1 on 1 session

================================================================================
"""

    with open(schedule_path, 'w') as f:
        f.write(schedule_content)

    print(f"✅ Schedule file created: {schedule_path}")
    print(f"📅 Schedule covers week of {monday.strftime('%m/%d/%Y')}")

    return schedule_path

if __name__ == "__main__":
    create_text_schedule()
