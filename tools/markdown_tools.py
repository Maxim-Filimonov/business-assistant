"""
Markdown Tools for CRM Operations
"""

from crewai.tools import BaseTool
import re
from typing import Dict, List, Optional
import os

class MarkdownReader(BaseTool):
    name: str = "Markdown Reader"
    description: str = "Reads and parses markdown files containing client information"

    def _run(self, file_path: str) -> str:
        """Read markdown file and return content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return f"File {file_path} not found"
        except Exception as e:
            return f"Error reading file: {str(e)}"

class MarkdownWriter(BaseTool):
    name: str = "Markdown Writer"
    description: str = "Writes or appends client information to markdown files"

    def _run(self, file_path: str, content: str, append: bool = True) -> str:
        """Write or append content to markdown file"""
        try:
            mode = 'a' if append else 'w'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, mode, encoding='utf-8') as f:
                if append and os.path.exists(file_path):
                    f.write('\n')
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

class ClientParser(BaseTool):
    name: str = "Client Parser"
    description: str = "Parses client information from markdown with flexible format handling"

    def _run(self, content: str, query: Optional[str] = None) -> Dict:
        """Parse client information from markdown content"""
        clients = {}
        current_client = None

        lines = content.split('\n')

        for line in lines:
            # Check for client header (## Name)
            if line.strip().startswith('##'):
                current_client = line.strip().replace('##', '').strip()
                clients[current_client] = {
                    'name': current_client,
                    'parent': None,
                    'phone': None,
                    'email': None,
                    'raw_data': []
                }
            elif current_client and line.strip():
                # Store raw data
                clients[current_client]['raw_data'].append(line.strip())

                # Try to parse structured data (flexible parsing)
                line_lower = line.lower()

                # Parent parsing
                if 'parent' in line_lower:
                    parent_match = re.search(r'parent[\s\-:]*(.+)', line, re.IGNORECASE)
                    if parent_match:
                        clients[current_client]['parent'] = parent_match.group(1).strip()

                # Phone parsing (various formats)
                phone_patterns = [
                    r'phone[\s\-:]*(\d+)',
                    r'tel[\s\-:]*(\d+)',
                    r'contact[\s\-:]*(\d+)',
                    r'number[\s\-:]*(\d+)',
                    r'(\d{7,})'  # Any sequence of 7+ digits
                ]
                for pattern in phone_patterns:
                    phone_match = re.search(pattern, line, re.IGNORECASE)
                    if phone_match:
                        clients[current_client]['phone'] = phone_match.group(1)
                        break

                # Email parsing
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
                if email_match:
                    clients[current_client]['email'] = email_match.group(0)

        # If query provided, filter results
        if query:
            query_lower = query.lower()
            filtered = {}
            for name, data in clients.items():
                if query_lower in name.lower():
                    filtered[name] = data
            return filtered

        return clients

class ClientSearcher(BaseTool):
    name: str = "Client Searcher"
    description: str = "Search for specific client information"

    def _run(self, client_name: str, clients_data: Dict) -> Dict:
        """Search for a specific client"""
        # Case-insensitive search
        for name, data in clients_data.items():
            if client_name.lower() in name.lower():
                return data
        return {'error': f'Client {client_name} not found'}

class ClientFormatter(BaseTool):
    name: str = "Client Formatter"
    description: str = "Formats client information for markdown storage"

    def _run(self, client_info: Dict) -> str:
        """Format client information as markdown"""
        name = client_info.get('name', 'Unknown')
        parent = client_info.get('parent', 'Not specified')
        phone = client_info.get('phone', 'Not specified')
        email = client_info.get('email', 'Not specified')

        formatted = f"""
## {name}
Parent - {parent}
Phone number {phone}
Email address {email}"""

        return formatted

class SafeMarkdownWriter(BaseTool):
    name: str = "Safe Markdown Writer"
    description: str = "Safely writes client information to markdown files, preventing data loss."

    def _run(self, file_path: str, old_content: str, new_content: str) -> str:
        """
        Safely write content to markdown file, preventing data loss.
        """
        try:
            # 1. Read the current content of the file
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()

            # 2. Compare old_content with current_content
            if old_content.strip() != current_content.strip():
                return (
                    "Error: The file has been modified since you last read it. "
                    "Please read the file again and re-apply your changes."
                )

            # 3. Use ClientParser to count clients
            parser = ClientParser()
            old_clients = parser._run(content=old_content)
            new_clients = parser._run(content=new_content)

            # 4. Check for data loss
            if len(new_clients) < len(old_clients):
                return (
                    f"Error: The new content has fewer clients ({len(new_clients)}) "
                    f"than the old content ({len(old_clients)}). "
                    "To prevent data loss, the write operation was aborted."
                )

            # 5. Write the new content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully wrote to {file_path}"

        except FileNotFoundError:
            # If the file doesn't exist, it's safe to write it.
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"Successfully created and wrote to {file_path}"

        except Exception as e:
            return f"Error writing file: {str(e)}"
