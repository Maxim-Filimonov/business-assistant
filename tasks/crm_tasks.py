"""
CRM Tasks - Define specific tasks for client management
"""

from crewai import Task

def search_client_task(agent, client_name, clients_file):
    """Task to search for client contact details"""
    return Task(
        description=f"""
        Search for the client named '{client_name}' in the CRM database.
        
        Steps:
        1. Read the markdown file at {clients_file}
        2. Parse the client information with flexible format handling
        3. Find the specific client (case-insensitive search)
        4. Extract and return their contact details including:
           - Full name
           - Parent/Guardian name
           - Phone number
           - Email address
        5. Handle any inconsistent data formats gracefully
        
        If the client is not found, provide a clear message.
        """,
        agent=agent,
        expected_output="Client contact details or 'not found' message"
    )

def add_client_task(agent, client_info, clients_file):
    """Task to add a new client to the CRM"""
    return Task(
        description=f"""
        Add a new client to the CRM database with the following information:
        - Name: {client_info.get('name')}
        - Parent: {client_info.get('parent')}
        - Phone: {client_info.get('phone')}
        - Email: {client_info.get('email')}
        
        Steps:
        1. Read the existing markdown file at {clients_file}
        2. Check if the client already exists (avoid duplicates)
        3. Format the new client information properly
        4. Append the new client to the markdown file
        5. Maintain consistent formatting with existing entries
        6. Confirm successful addition
        
        Handle missing or incomplete information appropriately.
        """,
        agent=agent,
        expected_output="Confirmation of client addition or error message"
    )

def query_parent_task(agent, client_name, clients_file):
    """Task to query parent name based on client name"""
    return Task(
        description=f"""
        Find the parent/guardian name for the client '{client_name}'.
        
        Steps:
        1. Read the markdown file at {clients_file}
        2. Parse all client information
        3. Search for the specific client (case-insensitive)
        4. Extract and return the parent/guardian name
        5. If multiple matches exist, list all possibilities
        
        Handle various formats like:
        - "Parent - John Doe"
        - "Guardian: Jane Smith"
        - "Parent/Guardian - Mike Johnson"
        """,
        agent=agent,
        expected_output="Parent/guardian name or 'not found' message"
    )

def update_client_task(agent, client_name, updates, clients_file):
    """Task to update existing client information"""
    return Task(
        description=f"""
        Update the information for client '{client_name}' with the following changes:
        {updates}
        
        Steps:
        1. Read the markdown file at {clients_file}
        2. Find the specific client entry
        3. Update the specified fields while preserving other information
        4. Rewrite the file with updated information
        5. Maintain markdown formatting consistency
        6. Confirm successful update
        
        Ensure data integrity and handle errors gracefully.
        """,
        agent=agent,
        expected_output="Confirmation of update or error message"
    )

def list_all_clients_task(agent, clients_file):
    """Task to list all clients in the database"""
    return Task(
        description=f"""
        List all clients currently in the CRM database.
        
        Steps:
        1. Read the markdown file at {clients_file}
        2. Parse all client entries
        3. Create a summary list with key information for each client:
           - Name
           - Parent (if available)
           - Contact status (has phone/email)
        4. Format the list clearly
        5. Include a total count of clients
        
        Handle any formatting inconsistencies in the source file.
        """,
        agent=agent,
        expected_output="Formatted list of all clients with summary information"
    )
