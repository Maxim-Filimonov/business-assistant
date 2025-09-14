"""
Dynamic Task Creation - Creates tasks based on natural language input
"""

from crewai import Task

def create_dynamic_task(agent, user_request, context=None):
    """
    Creates a dynamic task based on user's natural language request

    Args:
        agent: The agent that will execute the task
        user_request: The user's natural language request
        context: Additional context (file paths, settings, etc.)
    """

    # Build context string
    context_str = ""
    if context:
        if context.get('clients_file'):
            context_str += f"\nClients database location: {context['clients_file']}"
        if context.get('pricing_file'):
            context_str += f"\nPricing information location: {context['pricing_file']}"
        if context.get('schedule_pdf'):
            context_str += f"\nSchedule PDF location: {context['schedule_pdf']}"
        if context.get('invoice_template'):
            context_str += f"\nInvoice template location: {context['invoice_template']}"

    return Task(
        description=f"""
        User Request: {user_request}

        Your job is to understand and fulfill this request using your available tools
        and capabilities. Think step by step about what the user needs and how to
        accomplish it.

        {context_str}

        Be creative and thorough in your approach. If the request involves multiple
        steps or requires information from multiple sources, handle it intelligently.

        Always provide clear, helpful responses that directly address what the user asked for.
        """,
        agent=agent,
        expected_output="A clear, helpful response that fulfills the user's request"
    )

def create_dispatcher_task(dispatcher, user_request, available_agents, context=None):
    """
    Creates a task for the dispatcher to route and coordinate the request
    """

    agents_description = """
    Available specialized agents:
    1. CRM Agent - Handles all client-related tasks:
       - Search, add, update, delete clients
       - Find relationships (parents, guardians, contacts)
       - Manage contact information
       - Analyze client patterns or statistics

    2. Scheduler Agent - Manages time and appointments:
       - Extract schedules from PDFs
       - Find available time slots
       - Check conflicts
       - Organize appointments by specialist or client

    3. Invoice Agent - Handles billing and financial tasks:
       - Generate invoices
       - Calculate session costs
       - Apply pricing rules
       - Format bills professionally
    """

    context_str = ""
    if context:
        context_str = f"""
        Available resources:
        - Clients database: {context.get('clients_file', 'Not set')}
        - Pricing information: {context.get('pricing_file', 'Not set')}
        - Schedule PDF: {context.get('schedule_pdf', 'Not set')}
        - Invoice template: {context.get('invoice_template', 'Not set')}
        """

    return Task(
        description=f"""
        User Request: "{user_request}"

        {agents_description}

        {context_str}

        Your task:
        1. Understand what the user is trying to accomplish
        2. Determine which agent(s) can best handle this request
        3. Create a plan for how to fulfill the request
        4. Coordinate with the appropriate agent(s) to execute the plan
        5. Provide a comprehensive response to the user

        Be creative - the user might be asking for something we haven't explicitly
        programmed. Use the agents' capabilities creatively to solve new problems.

        Examples of creative solutions:
        - "Show me all clients whose parents have Gmail addresses" - Use CRM to search and filter
        - "Which specialist is busiest next week?" - Use Scheduler to analyze workload
        - "Create a summary report for last month" - Combine multiple agents' outputs
        """,
        agent=dispatcher,
        expected_output="A complete fulfillment of the user's request with clear results"
    )
