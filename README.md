# CrewAI Business Automation Application

A comprehensive business automation system built with CrewAI that combines CRM, Scheduling, and Invoice Generation capabilities.

## Features

### 1. CRM (Client Relationship Management)
- **Markdown-based storage** for easy editing and version control
- **Flexible data parsing** handles inconsistent input formats
- **Search functionality** to find client contact details quickly
- **Parent/Guardian queries** based on client names
- **Add new clients** with automatic formatting
- **Update existing client** information

### 2. Scheduler
- **PDF extraction** reads schedule documents automatically
- **Specialist filtering** shows only relevant appointments
- **Session parsing** extracts dates, times, and client names
- **Week filtering** for specific time periods
- **Multi-specialist support** for complex schedules

### 3. Invoice Maker
- **Automated billing** based on schedule data
- **Flexible pricing** supports multiple session types
- **Template-based** generation for consistent formatting
- **Weekly invoices** with detailed session breakdowns
- **Batch processing** for multiple specialists

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crewai_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Project Structure

```
crewai_app/
├── main.py                 # Main orchestration and crew management
├── agents/
│   ├── crm_agent.py       # CRM specialist agent
│   ├── scheduler_agent.py  # Schedule extraction agent
│   └── invoice_agent.py    # Invoice generation agent
├── tasks/
│   ├── crm_tasks.py       # CRM-related task definitions
│   ├── scheduler_tasks.py  # Scheduling task definitions
│   └── invoice_tasks.py    # Invoice task definitions
├── tools/
│   ├── markdown_tools.py   # Markdown parsing and writing tools
│   ├── pdf_tools.py        # PDF extraction and parsing tools
│   └── invoice_tools.py    # Invoice generation tools
├── data/
│   ├── clients.md          # Client database (markdown)
│   ├── pricing.md          # Pricing information
│   └── schedule.pdf        # Schedule documents (user-provided)
├── templates/
│   └── invoice_template.md # Invoice template
└── output/                  # Generated invoices and reports
```

## Usage

### Basic Usage

```python
from main import BusinessAutomationCrew

# Initialize the crew
crew = BusinessAutomationCrew(
    clients_file="data/clients.md",
    pricing_file="data/pricing.md",
    schedule_pdf="data/schedule.pdf",
    invoice_template="templates/invoice_template.md"
)

# Search for a client
result = crew.search_client("John Doe")
print(result)

# Add a new client
new_client = {
    "name": "Jane Smith",
    "parent": "Michael Smith",
    "phone": "92234567",
    "email": "jane@example.com"
}
result = crew.add_new_client(new_client)

# Get specialist schedule
schedule = crew.get_specialist_schedule("Dr. Johnson")

# Generate weekly invoice
invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=1)
```

### CRM Functions

#### Search Client
```python
result = crew.search_client("John Doe")
# Returns: Contact details including name, parent, phone, email
```

#### Add Client
```python
client_info = {
    "name": "New Client",
    "parent": "Parent Name",
    "phone": "12345678",
    "email": "client@email.com"
}
result = crew.add_new_client(client_info)
```

#### Find Parent
```python
parent = crew.find_parent("John Doe")
# Returns: "Jessy Queen"
```

### Scheduler Functions

#### Get Specialist Schedule
```python
schedule = crew.get_specialist_schedule("Dr. Johnson")
# Returns: List of all sessions for Dr. Johnson
```

### Invoice Functions

#### Generate Weekly Invoice
```python
# Generate invoice for last week (week_offset=1)
invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=1)
```

## Data Formats

### Client Markdown Format
The CRM system handles various formats flexibly:

```markdown
## Client Name
Parent - Parent Name
Phone number 12345678
Email address client@email.com
```

Alternative formats also supported:
- `Phone: 12345678`
- `Tel: 12345678`
- `Contact number: 12345678`
- `Guardian - Name` (instead of Parent)

### Pricing Markdown Format
```markdown
## Session Types
- 1 on 1 session - $50
- Group session - $100
```

### Schedule PDF Requirements
The system can parse PDFs with:
- Specialist names (Dr., Ms., Mr., etc.)
- Dates in various formats (MM/DD/YYYY, DD/MM/YYYY)
- Times in 12-hour format (10:00 AM, 2:30 PM)
- Client names following the time

Example PDF content:
```
Dr. Johnson
01/15/2025
10:00 AM - John Doe (1 on 1 session)
11:00 AM - Sarah Miller (Group session)
2:00 PM - Tommy Johnson (1 on 1 session)
```

## Advanced Features

### Batch Processing
Process multiple specialists at once:

```python
specialists = ["Dr. Johnson", "Dr. Smith", "Ms. Williams"]
for specialist in specialists:
    invoice = crew.generate_weekly_invoice(specialist)
    print(f"Invoice for {specialist}: {invoice}")
```

### Custom Week Ranges
Generate invoices for different weeks:

```python
# Current week
current_week_invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=0)

# Two weeks ago
two_weeks_ago_invoice = crew.generate_weekly_invoice("Dr. Johnson", week_offset=2)
```

### Error Handling
The system includes robust error handling:

```python
try:
    result = crew.search_client("NonExistent Client")
except Exception as e:
    print(f"Error: {e}")
```

## Customization

### Adding New Session Types
Edit `data/pricing.md`:

```markdown
- New session type - $80
```

### Modifying Invoice Template
Edit `templates/invoice_template.md` to customize invoice appearance.

### Extending Agents
Create new agents in `agents/` directory:

```python
from crewai import Agent

def custom_agent():
    return Agent(
        role='Custom Role',
        goal='Custom Goal',
        backstory='Custom Backstory',
        tools=[],
        verbose=True
    )
```

## Best Practices

1. **Regular Backups**: Keep backups of `data/clients.md`
2. **PDF Quality**: Ensure PDFs are text-searchable (not scanned images)
3. **Consistent Naming**: Use consistent specialist names across documents
4. **Data Validation**: Regularly validate client and pricing data
5. **Invoice Review**: Review generated invoices before sending

## Troubleshooting

### Common Issues

1. **PDF not reading correctly**
   - Ensure PDF contains searchable text
   - Try different PDF tools (PyPDF2 vs pdfplumber)

2. **Client not found**
   - Check spelling and case sensitivity
   - Verify client exists in markdown file

3. **Invoice calculations incorrect**
   - Verify pricing file is up to date
   - Check session type matching

4. **Memory issues with large PDFs**
   - Process schedules in batches
   - Use week filtering to reduce data

## API Requirements

This application requires:
- OpenAI API key for CrewAI agents
- Python 3.8 or higher
- All dependencies in requirements.txt

## Contributing

To extend the system:

1. Add new tools in `tools/` directory
2. Create corresponding tasks in `tasks/`
3. Define new agents if needed
4. Update main orchestration in `main.py`

## License

[Your License Here]

## Support

For issues or questions:
- Check the troubleshooting section
- Review example usage in `main.py`
- Ensure all data files are properly formatted

## Future Enhancements

Planned features:
- Database integration (PostgreSQL/MongoDB)
- Web interface with FastAPI
- Email integration for invoice delivery
- Appointment reminders
- Client portal
- Analytics dashboard
- Multi-language support
- Cloud storage integration
