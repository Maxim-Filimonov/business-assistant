# Business Automation Chat Interface

## Overview
This is an interactive chat application that uses CrewAI agents to help manage:
- **CRM**: Client information and contacts
- **Scheduling**: Extract and manage schedules from PDFs
- **Invoicing**: Generate invoices based on sessions and pricing

## Running the Chat

```bash
python main.py
```

## Chat Commands

The chat understands natural language. Here are some examples:

### Client Management
- `search John Doe` - Find client information
- `find Jane Smith` - Search for a client
- `add client` - Add a new client (interactive prompts)
- `who is the parent of John Doe` - Find parent/guardian

### Schedule Management
- `schedule for Dr. Johnson` - Get specialist's schedule
- `appointments for Dr. Smith` - View appointments

### Invoice Generation
- `generate invoice for Dr. Johnson` - Create weekly invoice
- `create invoice for Dr. Smith` - Generate billing

### Settings
- `set schedule pdf data/schedule.pdf` - Set PDF file path
- `set clients file data/clients.md` - Set clients database

### Other Commands
- `help` or `?` - Show available commands
- `exit`, `quit`, or `bye` - Exit the chat

## Examples

```
💬 You: search John Doe
🔍 Searching for client: John Doe
[Agent processes the request...]

💬 You: who is the parent of Jane Smith
🔍 Finding parent of: Jane Smith
[Agent finds and returns parent information...]

💬 You: generate invoice for Dr. Johnson
💰 Generating invoice for: Dr. Johnson
Week offset (1=last week, 2=two weeks ago) [default: 1]: 1
[Agent generates the invoice...]
```

## File Structure

Default file locations:
- **Clients database**: `data/clients.md`
- **Pricing information**: `data/pricing.md`
- **Schedule PDF**: `data/schedule.pdf`
- **Invoice template**: `templates/invoice_template.md`

You can change these paths using the `set` commands in the chat.

## Tips

1. The chat understands variations of commands:
   - "search", "find", "lookup", "get" all work for searching
   - "parent", "guardian" both work for finding parents

2. Client names are case-insensitive for searching

3. When adding clients, you'll be prompted for:
   - Name
   - Parent/Guardian name
   - Phone number
   - Email address

4. Invoice generation automatically:
   - Extracts schedule from PDF
   - Calculates sessions for the specified week
   - Applies pricing rules
   - Formats the invoice

## Troubleshooting

- **"No schedule PDF provided"**: Use `set schedule pdf [path]` to set the PDF file
- **"Client not found"**: Check spelling or use partial name search
- **LLM errors**: Check your API key configuration (see README_LLM_CONFIG.md)