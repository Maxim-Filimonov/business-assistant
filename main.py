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
from config import get_llm

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

        # Create a meta-agent that can understand and route any request
        self.orchestrator = self._create_orchestrator()

    def _create_orchestrator(self):
        """Create an intelligent orchestrator that decides which agents to use"""
        from crewai import Agent

        return Agent(
            role='Intelligent Request Analyzer and Orchestrator',
            goal='Analyze user requests and intelligently coordinate the right agents to fulfill them',
            backstory=f"""You are an intelligent orchestrator with deep understanding of business operations.
            You have access to three specialized teams:

            1. CRM Team: Manages client data from {self.context['clients_file']}
               - Client information (names, contacts, parents, emails, phones)
               - Client relationships and notes
               - Client search and filtering capabilities

            2. Scheduling Team: Manages appointments from {self.context.get('schedule_pdf', 'schedule PDFs')}
               - Specialist schedules and availability
               - Client appointments and sessions
               - Time-based queries and analysis

            3. Invoice Team: Manages financial data using {self.context['pricing_file']}
               - Invoice generation
               - Pricing and cost calculations
               - Financial reporting

            Your job is to:
            1. Analyze the user's request deeply
            2. Determine which teams need to be involved
            3. Decide if teams need to work together (cross-reference data)
            4. Create a plan for fulfilling the request

            You DON'T rely on keywords. Instead, you understand INTENT and CONTEXT.

            For example:
            - "Who are the parents of the morning clients?" requires BOTH schedule (to find morning clients) AND CRM (to get parents)
            - "List everyone" might mean clients (CRM) or appointments (Schedule) - you decide based on context
            - "What's the workload?" could need Schedule analysis
            - "Contact info for recent sessions" needs Schedule first, then CRM

            Think step-by-step about what information is needed and which agents can provide it.""",
            llm=get_llm(),
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=True
        )

    def process_request(self, user_request):
        """
        Process ANY user request using intelligent orchestration
        """
        # First, let the orchestrator analyze the request
        analysis_task = Task(
            description=f"""Analyze this request and determine how to fulfill it:

            User Request: {user_request}

            Provide a detailed analysis:
            1. What is the user asking for? (intent, not keywords)
            2. What information is needed to answer this?
            3. Which agents need to be involved?
            4. Do agents need to share data (cross-reference)?
            5. What's the logical order of operations?

            Be specific about:
            - If CRM is needed: what client data?
            - If Schedule is needed: what time period/specialist?
            - If Invoice is needed: what financial info?
            - If multiple agents: how do they connect?

            Output a clear execution plan.""",
            agent=self.orchestrator,
            expected_output="Detailed analysis and execution plan"
        )

        # Run the analysis
        analysis_crew = Crew(
            agents=[self.orchestrator],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )

        try:
            analysis = analysis_crew.kickoff()

            # Based on the analysis, execute the appropriate workflow
            return self._execute_based_on_analysis(user_request, str(analysis))

        except Exception as e:
            return f"Error analyzing request: {str(e)}"

    def _execute_based_on_analysis(self, user_request, analysis):
        """
        Execute the appropriate workflow based on orchestrator's analysis
        """
        analysis_lower = analysis.lower()

        # Determine which agents are needed based on the analysis
        needs_crm = any(term in analysis_lower for term in
                       ['crm', 'client data', 'parent', 'contact', 'client information'])
        needs_schedule = any(term in analysis_lower for term in
                           ['schedule', 'appointment', 'specialist', 'time period', 'sessions'])
        needs_invoice = any(term in analysis_lower for term in
                          ['invoice', 'financial', 'pricing', 'billing', 'cost'])

        # Check if cross-referencing is needed
        needs_cross_reference = ('cross-reference' in analysis_lower or
                                'share data' in analysis_lower or
                                'both' in analysis_lower or
                                'combine' in analysis_lower or
                                (needs_crm and needs_schedule))

        print(f"\n📊 Analysis complete:")
        print(f"   - Needs CRM: {needs_crm}")
        print(f"   - Needs Schedule: {needs_schedule}")
        print(f"   - Needs Invoice: {needs_invoice}")
        print(f"   - Needs Cross-Reference: {needs_cross_reference}")

        if needs_cross_reference:
            return self._execute_cross_reference(user_request, analysis)
        elif needs_crm:
            return self._execute_crm_task(user_request)
        elif needs_schedule:
            return self._execute_schedule_task(user_request)
        elif needs_invoice:
            return self._execute_invoice_task(user_request)
        else:
            return f"Based on analysis, I understand you're asking: '{user_request}'\n\nAnalysis:\n{analysis}\n\nPlease provide more specific details about what you need."

    def _execute_cross_reference(self, user_request, analysis):
        """
        Handle requests that need data from multiple agents
        """
        print("\n🔄 Executing cross-agent coordination based on analysis...")

        tasks = []
        agents_list = []

        # Determine task order based on analysis
        if 'schedule' in analysis.lower() and 'crm' in analysis.lower():
            # Schedule -> CRM flow (most common)
            schedule_task = Task(
                description=f"""Based on this request: {user_request}

                Extract the relevant schedule information:
                - Identify the specialist/doctor mentioned
                - Determine the time period
                - List ALL relevant client names

                Return a clear list of findings.""",
                agent=self.scheduler,
                expected_output="Schedule findings and client list"
            )
            tasks.append(schedule_task)
            agents_list.append(self.scheduler)

            crm_task = Task(
                description=f"""Using the schedule data from the previous task:

                Original request: {user_request}

                Extract the relevant CRM information for each client found:
                - Read the CRM database once
                - Match ALL clients from the schedule
                - Extract requested information (parents, contacts, etc.)

                Provide complete information for ALL relevant clients.""",
                agent=self.crm,
                expected_output="Complete CRM data for all relevant clients",
                context=[schedule_task]
            )
            tasks.append(crm_task)
            agents_list.append(self.crm)

        # Add more cross-reference patterns as needed

        # Create crew with proper task dependencies
        crew = Crew(
            agents=agents_list,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            full_output=True
        )

        try:
            result = crew.kickoff()
            return f"Based on coordinated analysis:\n\n{result}"
        except Exception as e:
            return f"Error in cross-agent coordination: {str(e)}"

    def _execute_crm_task(self, user_request):
        """Execute a CRM-only task"""
        print("\n📋 Executing CRM task...")

        task = Task(
            description=f"Handle this request using CRM data: {user_request}",
            agent=self.crm,
            expected_output="Complete CRM information as requested"
        )

        crew = Crew(
            agents=[self.crm],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return f"CRM Data:\n{result}"
        except Exception as e:
            return f"CRM Error: {str(e)}"

    def _execute_schedule_task(self, user_request):
        """Execute a Schedule-only task"""
        print("\n📅 Executing Schedule task...")

        task = Task(
            description=f"Handle this request using schedule data: {user_request}",
            agent=self.scheduler,
            expected_output="Complete schedule information as requested"
        )

        crew = Crew(
            agents=[self.scheduler],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return f"Schedule Data:\n{result}"
        except Exception as e:
            return f"Schedule Error: {str(e)}"

    def _execute_invoice_task(self, user_request):
        """Execute an Invoice-only task"""
        print("\n💰 Executing Invoice task...")

        task = Task(
            description=f"Handle this request using invoice/financial data: {user_request}",
            agent=self.invoicer,
            expected_output="Complete invoice/financial information as requested"
        )

        crew = Crew(
            agents=[self.invoicer],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return f"Invoice Data:\n{result}"
        except Exception as e:
            return f"Invoice Error: {str(e)}"

class UltraFlexibleChat:
    def __init__(self):
        self.system = FlexibleBusinessChat()
        self.history = []

    def run(self):
        """Run the ultra-flexible chat"""
        print("\n" + "="*70)
        print("🧠 INTELLIGENT BUSINESS AI ASSISTANT")
        print("="*70)
        print("\nI understand context and intent, not just keywords!")
        print("Ask me anything about your business operations.")
        print("\nExamples of what you can ask:")
        print("  • 'Who are the parents of morning appointments?'")
        print("  • 'List everyone' (I'll figure out what you mean)")
        print("  • 'What's the workload distribution?'")
        print("  • 'Contact details for this week's sessions'")
        print("  • 'Analysis of specialist availability'")
        print("  • Or any complex query that combines different data sources!")
        print("\nType 'exit' to leave")
        print("="*70)

        while True:
            try:
                user_input = input("\n💭 What would you like to know? ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n✨ Thanks for using the Intelligent AI Assistant! Goodbye!")
                    break

                # Store in history
                self.history.append({"user": user_input})

                # Process with intelligent orchestration
                print("\n🧠 Analyzing your request intelligently...")
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
