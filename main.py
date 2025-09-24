#!/usr/bin/env python
"""
Ultra-Flexible CrewAI Business Chat
Agents can interpret and execute any request creatively
"""

import sys
from crewai import Crew, Process, Task
from agents.crm_agent import crm_agent
from agents.scheduler_agent import scheduler_agent
from agents.invoice_agent import invoice_agent
from agents.dispatcher_agent import dispatcher_agent
from tasks.dynamic_tasks import create_dispatcher_task
from config import get_llm
from orchestrator import PlanningOrchestrator

class FlexibleBusinessChat:
    def __init__(self,
                 clients_file="data/clients.md",
                 pricing_file="data/pricing.md",
                 schedule_pdf="data/sample_schedule.pdf",
                 invoice_template="templates/invoice_template.md"):
        """
        Initialize the ultra-flexible chat system
        """
        self.context = {
            'clients_file': clients_file,
            'pricing_file': pricing_file,
            'schedule_pdf': schedule_pdf,
            'invoice_template': invoice_template
        }

        # Initialize agents
        self.crm = crm_agent(clients_file=self.context['clients_file'])
        self.scheduler = scheduler_agent(schedule_pdf=self.context.get('schedule_pdf'))
        self.invoicer = invoice_agent()
        self._crew_cls = Crew
        self._dispatcher_factory = dispatcher_agent
        self.orchestrator = PlanningOrchestrator(
            dispatcher_factory=self._dispatcher_factory,
            crew_cls=self._crew_cls,
            llm_provider=get_llm,
        )

        # Create a meta-agent that can understand and route any request
        self.meta_agent = self._create_meta_agent()

    def _create_meta_agent(self):
        """Create a meta-agent that understands context and coordinates everything"""
        from crewai import Agent

        return Agent(
            role='Business Operations Orchestrator',
            goal='Understand and fulfill any business-related request by creatively using available agents and tools',
            backstory=f"""You are an intelligent orchestrator with access to three specialized teams:

            1. CRM Team: Manages ALL client-related data. They have access to {self.context['clients_file']}.
               They can search, add, update, analyze, and create reports about clients.

            2. Scheduling Team: Handles ALL time-related tasks. They work with {self.context.get('schedule_pdf', 'schedule PDFs')}.
               They can extract schedules, find patterns, analyze workload, and identify conflicts.

            3. Invoice Team: Manages ALL financial tasks. They use {self.context['pricing_file']} and {self.context['invoice_template']}.
               They can generate invoices, calculate costs, analyze revenue, and create financial reports.

            You are CREATIVE and INTELLIGENT. When users ask for something unusual, you figure out how to
            accomplish it using your teams. You can combine multiple teams' capabilities to solve complex problems.

            Examples of creative problem-solving:
            - "Who hasn't been scheduled this month?" - Use CRM to get all clients, Scheduler to check appointments
            - "What's our busiest day?" - Use Scheduler to analyze patterns
            - "Show me clients with overdue payments" - Combine CRM and Invoice data
            - "Create a report of all Gmail users" - Use CRM to filter by email domain

            You think step-by-step and aren't limited by pre-programmed commands. You interpret
            the user's intent and find creative ways to fulfill it.""",
            llm=get_llm(),
            verbose=True,
            allow_delegation=True,  # Enable delegation
            max_iter=3,
            memory=True
        )

    def process_request(self, user_request):
        """
        Process ANY user request by creating a dynamic task
        """
        try:
            return self._process_with_orchestrator(user_request)
        except Exception:
            return self._process_fallback(user_request)

    def _process_with_orchestrator(self, user_request):
        """Process the request using a planning-enabled orchestrator crew."""
        result = self.orchestrator.dispatch(
            user_request=user_request,
            agents=[self.crm, self.scheduler, self.invoicer],
            context=self.context,
        )
        return self._extract_response(result)

    def _process_sequential(self, user_request):
        """
        Process request using sequential approach to avoid delegation validation errors
        """
        # Create a simple task for the meta agent without delegation
        task = Task(
            description=f"Analyze this request and determine what information is needed: {user_request}",
            agent=self.meta_agent,
            expected_output="Analysis of what information is needed and which agents should be involved"
        )

        # Create a crew with sequential processing (no delegation)
        crew = Crew(
            agents=[self.meta_agent, self.crm, self.scheduler, self.invoicer],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
            memory=True,
            full_output=True
        )

        return crew.kickoff()

    def _process_fallback(self, user_request):
        """
        Fallback method that directly calls agents without crew delegation
        """
        # Analyze the request to determine which agents to use
        request_lower = user_request.lower()

        response_parts = []

        # Check if CRM-related
        if any(keyword in request_lower for keyword in ['client', 'customer', 'contact', 'phone', 'email', 'parent']):
            try:
                # Create a simple task for CRM
                crm_task = Task(
                    description=f"Handle this CRM-related request: {user_request}",
                    agent=self.crm,
                    expected_output="CRM information or analysis"
                )
                crm_crew = self._crew_cls(agents=[self.crm], tasks=[crm_task], process=Process.sequential, verbose=True)
                crm_result = self._extract_response(crm_crew.kickoff())
                response_parts.append(f"CRM Analysis: {crm_result}")
            except Exception as e:
                response_parts.append(f"CRM processing encountered an issue: {e}")

        # Check if schedule-related
        if any(keyword in request_lower for keyword in ['schedule', 'appointment', 'time', 'week', 'day', 'session']):
            try:
                schedule_task = Task(
                    description=f"Handle this scheduling request: {user_request}",
                    agent=self.scheduler,
                    expected_output="Schedule information or analysis"
                )
                schedule_crew = self._crew_cls(agents=[self.scheduler], tasks=[schedule_task], process=Process.sequential, verbose=True)
                schedule_result = self._extract_response(schedule_crew.kickoff())
                response_parts.append(f"Schedule Analysis: {schedule_result}")
            except Exception as e:
                response_parts.append(f"Schedule processing encountered an issue: {e}")

        # Check if invoice-related
        if any(keyword in request_lower for keyword in ['invoice', 'billing', 'payment', 'cost', 'price', 'money']):
            try:
                invoice_task = Task(
                    description=f"Handle this invoice-related request: {user_request}",
                    agent=self.invoicer,
                    expected_output="Invoice information or analysis"
                )
                invoice_crew = self._crew_cls(agents=[self.invoicer], tasks=[invoice_task], process=Process.sequential, verbose=True)
                invoice_result = self._extract_response(invoice_crew.kickoff())
                response_parts.append(f"Invoice Analysis: {invoice_result}")
            except Exception as e:
                response_parts.append(f"Invoice processing encountered an issue: {e}")

        if not response_parts:
            return f"I understand you're asking: '{user_request}'. However, I need more specific information about clients, schedules, or invoicing to help you effectively."

        return "\n\n".join(response_parts)

    @staticmethod
    def _extract_response(result):
        """Normalize Crew outputs to a simple string for the chat response."""
        if isinstance(result, dict):
            for key in ("final_output", "output", "result"):
                if key in result:
                    return result[key]
        return result

class UltraFlexibleChat:
    def __init__(self):
        self.system = FlexibleBusinessChat()
        self.history = []

    def run(self):
        """Run the ultra-flexible chat"""
        print("\n" + "="*70)
        print("🧠 ULTRA-FLEXIBLE BUSINESS AI ASSISTANT")
        print("="*70)
        print("\nI'm not limited to pre-programmed commands!")
        print("Ask me ANYTHING about your business operations.")
        print("\nExamples of what you can ask:")
        print("  • 'Find all clients whose parents have Gmail'")
        print("  • 'Who hasn't had an appointment in 2 weeks?'")
        print("  • 'Compare this week's schedule to last week'")
        print("  • 'Which clients might need follow-ups?'")
        print("  • 'Create a summary of our busiest specialists'")
        print("  • Or anything else you can think of!")
        print("\nType 'exit' to leave")
        print("="*70)

        while True:
            try:
                user_input = input("\n💭 What would you like to know? ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n✨ Thanks for using the Ultra-Flexible AI! Goodbye!")
                    break

                # Store in history
                self.history.append({"user": user_input})

                # Process with full flexibility
                print("\n🧠 Thinking creatively about your request...")
                print("(The AI agents are collaborating to find the best solution)\n")

                result = self.system.process_request(user_input)

                # Store result
                self.history.append({"assistant": str(result)})

                # Display result
                print("\n" + "="*70)
                print("💡 Here's what I found:")
                print("="*70)
                print(result)

            except KeyboardInterrupt:
                print("\n\n✨ Goodbye!")
                break
            except Exception as e:
                print(f"\n⚠️ Unexpected issue: {e}")
                print("Feel free to rephrase or try a different question!")

def main():
    chat = UltraFlexibleChat()
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"\n💭 What would you like to know? {user_input}")
        result = chat.system.process_request(user_input)
        print("\n" + "="*70)
        print("💡 Here's what I found:")
        print("="*70)
        print(result)
    else:
        chat.run()

if __name__ == "__main__":
    main()
