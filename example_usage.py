"""
Example Usage Script for CrewAI Business Automation Application
This script demonstrates all major functions of the system.
"""

from main import BusinessAutomationCrew
import os
from datetime import datetime

def demo_crm_functions(crew):
    """Demonstrate CRM capabilities"""
    print("\n" + "="*50)
    print("CRM DEMONSTRATION")
    print("="*50)
    
    # 1. Search for existing client
    print("\n1. Searching for client 'John Doe'...")
    result = crew.search_client("John Doe")
    print(f"Result: {result}")
    
    # 2. Find parent/guardian
    print("\n2. Finding parent for 'Sarah Miller'...")
    parent = crew.find_parent("Sarah Miller")
    print(f"Parent: {parent}")
    
    # 3. Add new client
    print("\n3. Adding new client 'Alex Thompson'...")
    new_client = {
        "name": "Alex Thompson",
        "parent": "Patricia Thompson",
        "phone": "92999888",
        "email": "alex.t@example.com"
    }
    result = crew.add_new_client(new_client)
    print(f"Result: {result}")
    
    # 4. Handle inconsistent input
    print("\n4. Adding client with inconsistent format...")
    messy_client = {
        "name": "Billy Chen",
        "parent": "David Chen",
        "phone": "Contact: 92888777",  # Inconsistent format
        "email": "billy chen @ email . com"  # Spaces in email
    }
    result = crew.add_new_client(messy_client)
    print(f"Result: {result}")

def demo_scheduler_functions(crew):
    """Demonstrate Scheduler capabilities"""
    print("\n" + "="*50)
    print("SCHEDULER DEMONSTRATION")
    print("="*50)
    
    # Note: This requires a PDF file to be present
    if not os.path.exists("data/schedule.pdf"):
        print("\nNote: Schedule PDF not found. Creating sample schedule data...")
        create_sample_schedule_text()
        return
    
    # 1. Get specialist schedule
    print("\n1. Extracting schedule for 'Dr. Johnson'...")
    schedule = crew.get_specialist_schedule("Dr. Johnson")
    print(f"Schedule: {schedule}")
    
    # 2. Get another specialist
    print("\n2. Extracting schedule for 'Ms. Williams'...")
    schedule = crew.get_specialist_schedule("Ms. Williams")
    print(f"Schedule: {schedule}")

def demo_invoice_functions(crew):
    """Demonstrate Invoice Generation capabilities"""
    print("\n" + "="*50)
    print("INVOICE GENERATION DEMONSTRATION")
    print("="*50)
    
    # 1. Generate invoice for last week
    print("\n1. Generating invoice for 'Dr. Johnson' (last week)...")
    invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=1)
    print(f"Invoice generated:\n{invoice}")
    
    # 2. Generate invoice for current week
    print("\n2. Generating invoice for 'Dr. Johnson' (current week)...")
    invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=0)
    print(f"Invoice generated:\n{invoice}")

def create_sample_schedule_text():
    """Create a sample schedule text file (when PDF is not available)"""
    sample_schedule = """
WEEKLY SCHEDULE

Dr. Johnson
Monday, 01/13/2025
9:00 AM - John Doe (1 on 1 session)
10:00 AM - Sarah Miller (1 on 1 session)
11:00 AM - Group Session - Tommy Johnson, Emma Wilson, Lucas Brown
2:00 PM - Sophia Davis (1 on 1 session)

Tuesday, 01/14/2025
9:00 AM - Emma Wilson (1 on 1 session)
10:00 AM - John Doe (1 on 1 session)
2:00 PM - Group Session - Sarah Miller, Tommy Johnson

Ms. Williams
Monday, 01/13/2025
9:00 AM - Lucas Brown (1 on 1 session)
10:00 AM - Tommy Johnson (1 on 1 session)
3:00 PM - Emma Wilson (1 on 1 session)

Tuesday, 01/14/2025
10:00 AM - Group Session - John Doe, Sophia Davis
2:00 PM - Sarah Miller (1 on 1 session)

Dr. Smith
Wednesday, 01/15/2025
9:00 AM - John Doe (Assessment session)
11:00 AM - Sarah Miller (1 on 1 session)
2:00 PM - Family session - Tommy Johnson family
"""
    
    # Save as text file (PDF conversion would require additional libraries)
    with open("data/sample_schedule.txt", "w") as f:
        f.write(sample_schedule)
    print("Sample schedule created at data/sample_schedule.txt")
    print("Note: For full functionality, convert this to PDF format")

def run_full_demo():
    """Run complete demonstration of all features"""
    print("\n" + "="*60)
    print("CREWAI BUSINESS AUTOMATION - FULL DEMONSTRATION")
    print("="*60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize the crew
    print("\nInitializing Business Automation Crew...")
    crew = BusinessAutomationCrew(
        clients_file="data/clients.md",
        pricing_file="data/pricing.md",
        schedule_pdf="data/schedule.pdf",  # You'll need to provide this
        invoice_template="templates/invoice_template.md"
    )
    print("✓ Crew initialized successfully")
    
    # Run demonstrations
    try:
        # CRM Demo
        demo_crm_functions(crew)
        
        # Scheduler Demo
        demo_scheduler_functions(crew)
        
        # Invoice Demo
        demo_invoice_functions(crew)
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Please ensure all required files are in place.")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)

def interactive_mode():
    """Run in interactive mode allowing user to choose functions"""
    print("\n" + "="*60)
    print("CREWAI BUSINESS AUTOMATION - INTERACTIVE MODE")
    print("="*60)
    
    crew = BusinessAutomationCrew(
        clients_file="data/clients.md",
        pricing_file="data/pricing.md",
        schedule_pdf="data/schedule.pdf",
        invoice_template="templates/invoice_template.md"
    )
    
    while True:
        print("\n" + "-"*40)
        print("Choose an option:")
        print("1. Search for client")
        print("2. Add new client")
        print("3. Find parent/guardian")
        print("4. Get specialist schedule")
        print("5. Generate invoice")
        print("6. Run full demo")
        print("0. Exit")
        print("-"*40)
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == "0":
            print("Exiting... Thank you!")
            break
            
        elif choice == "1":
            name = input("Enter client name to search: ").strip()
            result = crew.search_client(name)
            print(f"\nResult: {result}")
            
        elif choice == "2":
            print("\nEnter new client details:")
            name = input("Name: ").strip()
            parent = input("Parent/Guardian: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            
            new_client = {
                "name": name,
                "parent": parent,
                "phone": phone,
                "email": email
            }
            result = crew.add_new_client(new_client)
            print(f"\nResult: {result}")
            
        elif choice == "3":
            name = input("Enter client name to find parent: ").strip()
            result = crew.find_parent(name)
            print(f"\nParent/Guardian: {result}")
            
        elif choice == "4":
            specialist = input("Enter specialist name: ").strip()
            result = crew.get_specialist_schedule(specialist)
            print(f"\nSchedule: {result}")
            
        elif choice == "5":
            specialist = input("Enter specialist name: ").strip()
            week = input("Weeks ago (0=current, 1=last week): ").strip()
            try:
                week_offset = int(week)
                result = crew.generate_weekly_invoice(specialist, week_offset)
                print(f"\nInvoice:\n{result}")
            except ValueError:
                print("Invalid week offset. Please enter a number.")
                
        elif choice == "6":
            run_full_demo()
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        print("Starting automated demonstration...")
        print("(Run with --interactive flag for interactive mode)")
        run_full_demo()
