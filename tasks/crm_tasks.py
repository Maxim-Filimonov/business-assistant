"""CRM Tasks - Define specific tasks for SQLite-backed client management."""

from crewai import Task


def search_client_task(agent, client_name: str, db_path: str):
    """Task to search for client contact details."""

    return Task(
        description=f"""
        Search for the client named '{client_name}' in the CRM database.

        Steps:
        1. Use the CRM Client Reader tool pointed at {db_path}.
        2. Request the specific client (case-insensitive lookup).
        3. Return their structured details, including:
           - Full name
           - Parent/Guardian name
           - Phone number
           - Email address
           - Notes summary if present
        4. If the client is not found, provide a clear message.
        """,
        agent=agent,
        expected_output="Client contact details or 'not found' message",
    )


def add_client_task(agent, client_info: dict, db_path: str):
    """Task to add a new client to the CRM."""

    return Task(
        description=f"""
        Add a new client to the CRM database with the following information:
        - Name: {client_info.get('name')}
        - Parent: {client_info.get('parent')}
        - Phone: {client_info.get('phone')}
        - Email: {client_info.get('email')}
        - Notes (optional): {client_info.get('notes')}

        Steps:
        1. Run a diff preview for the proposed record using the CRM Client Diff Preview tool.
        2. Share the resulting diff with the user for approval.
        3. After explicit approval, call CRM Client Apply Update with the same payload.
        4. Confirm that the markdown snapshot was exported successfully.
        """,
        agent=agent,
        expected_output="Diff preview followed by confirmation of client addition once approved.",
    )


def query_parent_task(agent, client_name: str, db_path: str):
    """Task to query parent name based on client name."""

    return Task(
        description=f"""
        Find the parent/guardian name for the client '{client_name}'.

        Steps:
        1. Use the CRM Client Reader to fetch the specific client from {db_path}.
        2. Extract the parent/guardian information.
        3. If multiple matches exist, list all possibilities and highlight differences.
        4. Present the findings clearly for the user.
        """,
        agent=agent,
        expected_output="Parent/guardian name or 'not found' message",
    )


def update_client_task(agent, client_name: str, updates: dict, db_path: str):
    """Task to update existing client information."""

    return Task(
        description=f"""
        Update the information for client '{client_name}' with the following changes:
        {updates}

        Steps:
        1. Use the CRM Client Diff Preview tool to generate a unified diff of the proposed update.
        2. Share the diff with the user and wait for confirmation before making changes.
        3. Once approved, call CRM Client Apply Update with the exact payload.
        4. Confirm that the markdown export has been refreshed for the client.
        5. Report the final state back to the user.
        """,
        agent=agent,
        expected_output="Diff preview and confirmation of update once approved",
    )


def list_all_clients_task(agent, db_path: str):
    """Task to list all clients in the database."""

    return Task(
        description=f"""
        List all clients currently in the CRM database.

        Steps:
        1. Use the CRM Client Reader tool (without a specific name) targeting {db_path}.
        2. Summarize key information for each client:
           - Name
           - Parent (if available)
           - Contact status (has phone/email)
        3. Mention how to locate the generated markdown snapshots for human review.
        4. Provide the total count of clients.
        """,
        agent=agent,
        expected_output="Formatted list of all clients with summary information",
    )
