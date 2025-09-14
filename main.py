#!/usr/bin/env python
"""
CrewAI Multi-Function Business Chat Application CLI
Interactive chat interface for CRM, Scheduler, and Invoice functionality
"""

import sys
import re
from crewai import Crew, Process
from agents.crm_agent import crm_agent
from agents.scheduler_agent import scheduler_agent
from agents.invoice_agent import invoice_agent
from tasks.crm_tasks import (
    search_client_task,
    add_client_task,
    query_parent_task
)
from tasks.scheduler_tasks import extract_schedule_task
from tasks.invoice_tasks import generate_invoice_task
from datetime import datetime

class BusinessAutomationCrew:
    def __init__(self, clients_file="data/clients.md",
                 pricing_file="data/pricing.md",
                 schedule_pdf="data/schedule.pdf",
                 invoice_template="templates/invoice_template.md"):
        self.clients_file = clients_file
        self.pricing_file = pricing_file
        self.schedule_pdf = schedule_pdf
        self.invoice_template = invoice_template

        # Initialize agents
        self.crm = crm_agent()
        self.scheduler = scheduler_agent()
        self.invoicer = invoice_agent()

    def search_client(self, client_name):
        """Search for client contact details"""
        task = search_client_task(self.crm, client_name, self.clients_file)
        crew = Crew(
            agents=[self.crm],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()

    def add_new_client(self, client_info):
        """Add a new client to the CRM"""
        task = add_client_task(self.crm, client_info, self.clients_file)
        crew = Crew(
            agents=[self.crm],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()

    def find_parent(self, client_name):
        """Query for parent name based on client name"""
        task = query_parent_task(self.crm, client_name, self.clients_file)
        crew = Crew(
            agents=[self.crm],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()

    def get_specialist_schedule(self, specialist_name):
        """Extract schedule for a specific specialist from PDF"""
        if not self.schedule_pdf:
            return "No schedule PDF provided. Please set the schedule PDF path first."

        task = extract_schedule_task(
            self.scheduler,
            specialist_name,
            self.schedule_pdf
        )
        crew = Crew(
            agents=[self.scheduler],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()

    def generate_weekly_invoice(self, specialist_name, week_offset=1):
        """Generate invoice for last week's sessions"""
        if not self.schedule_pdf:
            return "No schedule PDF provided. Please set the schedule PDF path first."

        # First get the schedule
        schedule_task = extract_schedule_task(
            self.scheduler,
            specialist_name,
            self.schedule_pdf
        )

        # Then generate invoice
        invoice_task = generate_invoice_task(
            self.invoicer,
            specialist_name,
            self.pricing_file,
            self.invoice_template,
            week_offset
        )

        # Create a crew that runs both tasks in sequence
        crew = Crew(
            agents=[self.scheduler, self.invoicer],
            tasks=[schedule_task, invoice_task],
            process=Process.sequential,
            verbose=True,
            memory=True  # Enable memory to share context between tasks
        )

        return crew.kickoff()

class ChatInterface:
    def __init__(self):
        self.crew = BusinessAutomationCrew()
        self.commands_help = """
Available commands:
  • Search for a client: "search [client name]" or "find [client name]"
  • Add a new client: "add client [name]" then follow prompts
  • Find parent: "who is the parent of [client name]"
  • Get schedule: "schedule for [specialist name]"
  • Generate invoice: "generate invoice for [specialist name]"
  • Settings: "set schedule pdf [path]" or "set clients file [path]"
  • Help: "help" or "?"
  • Exit: "exit", "quit", or "bye"
        """

    def parse_command(self, user_input):
        """Parse natural language input to determine intent"""
        input_lower = user_input.lower().strip()

        # Exit commands
        if input_lower in ['exit', 'quit', 'bye', 'goodbye']:
            return 'exit', None

        # Help commands
        if input_lower in ['help', '?', 'commands']:
            return 'help', None

        # Search client
        if re.match(r'(search|find|lookup|get)\s+(client\s+)?(.+)', input_lower):
            match = re.match(r'(search|find|lookup|get)\s+(client\s+)?(.+)', input_lower)
            client_name = match.group(3)
            return 'search_client', client_name

        # Find parent
        if re.match(r'(who|what).*(parent|guardian).*(of|for)\s+(.+)', input_lower):
            match = re.match(r'(who|what).*(parent|guardian).*(of|for)\s+(.+)', input_lower)
            client_name = match.group(4)
            return 'find_parent', client_name

        # Add client
        if re.match(r'add\s+(client|person)\s*(.+)?', input_lower):
            match = re.match(r'add\s+(client|person)\s*(.+)?', user_input, re.IGNORECASE)
            client_name = match.group(2) if match.group(2) else None
            return 'add_client', client_name

        # Get schedule
        if re.match(r'(schedule|appointments?).*(for|of)\s+(.+)', input_lower):
            match = re.match(r'(schedule|appointments?).*(for|of)\s+(.+)', user_input, re.IGNORECASE)
            specialist = match.group(3)
            return 'get_schedule', specialist

        # Generate invoice
        if re.match(r'(generate|create|make)\s+invoice.*(for|of)\s+(.+)', input_lower):
            match = re.match(r'(generate|create|make)\s+invoice.*(for|of)\s+(.+)', user_input, re.IGNORECASE)
            specialist = match.group(3)
            return 'generate_invoice', specialist

        # Settings commands
        if re.match(r'set\s+schedule\s+pdf\s+(.+)', input_lower):
            match = re.match(r'set\s+schedule\s+pdf\s+(.+)', user_input, re.IGNORECASE)
            path = match.group(1)
            return 'set_schedule_pdf', path

        if re.match(r'set\s+clients?\s+file\s+(.+)', input_lower):
            match = re.match(r'set\s+clients?\s+file\s+(.+)', user_input, re.IGNORECASE)
            path = match.group(1)
            return 'set_clients_file', path

        return 'unknown', None

    def get_client_details(self):
        """Interactive prompt to get client details"""
        print("\nPlease provide client details:")
        name = input("Client name: ").strip()
        parent = input("Parent/Guardian name: ").strip()
        phone = input("Phone number: ").strip()
        email = input("Email address: ").strip()

        return {
            "name": name,
            "parent": parent,
            "phone": phone,
            "email": email
        }

    def run(self):
        """Main chat loop"""
        print("\n" + "="*60)
        print("🤖 Business Automation Assistant")
        print("="*60)
        print("\nHello! I'm your business automation assistant.")
        print("I can help you manage clients, schedules, and invoices.")
        print("\nType 'help' to see available commands or just tell me what you need!")
        print("="*60)

        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Parse command
                command, data = self.parse_command(user_input)

                # Execute command
                if command == 'exit':
                    print("\n👋 Goodbye! Have a great day!")
                    break

                elif command == 'help':
                    print(self.commands_help)

                elif command == 'search_client':
                    print(f"\n🔍 Searching for client: {data}")
                    result = self.crew.search_client(data)
                    print(f"\n📋 Result:\n{result}")

                elif command == 'find_parent':
                    print(f"\n🔍 Finding parent of: {data}")
                    result = self.crew.find_parent(data)
                    print(f"\n📋 Result:\n{result}")

                elif command == 'add_client':
                    if data:
                        print(f"\nAdding client: {data}")
                    client_info = self.get_client_details()
                    print(f"\n➕ Adding new client: {client_info['name']}")
                    result = self.crew.add_new_client(client_info)
                    print(f"\n📋 Result:\n{result}")

                elif command == 'get_schedule':
                    print(f"\n📅 Getting schedule for: {data}")
                    result = self.crew.get_specialist_schedule(data)
                    print(f"\n📋 Result:\n{result}")

                elif command == 'generate_invoice':
                    print(f"\n💰 Generating invoice for: {data}")
                    week_input = input("Week offset (1=last week, 2=two weeks ago) [default: 1]: ").strip()
                    week_offset = int(week_input) if week_input else 1
                    result = self.crew.generate_weekly_invoice(data, week_offset)
                    print(f"\n📋 Result:\n{result}")

                elif command == 'set_schedule_pdf':
                    self.crew.schedule_pdf = data
                    print(f"✅ Schedule PDF set to: {data}")

                elif command == 'set_clients_file':
                    self.crew.clients_file = data
                    print(f"✅ Clients file set to: {data}")

                else:
                    print("\n❓ I didn't understand that command.")
                    print("Type 'help' to see available commands or try rephrasing.")
                    print("\nExamples:")
                    print("  • 'search John Doe'")
                    print("  • 'who is the parent of Jane Smith'")
                    print("  • 'schedule for Dr. Johnson'")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! (Interrupted by user)")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Entry point for the chat application"""
    chat = ChatInterface()
    chat.run()

if __name__ == "__main__":
    main()
