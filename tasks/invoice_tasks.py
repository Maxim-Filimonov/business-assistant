"""
Invoice Tasks - Define tasks for invoice generation and billing
"""

from crewai import Task

def generate_invoice_task(agent, specialist_name, pricing_file, template_file, week_offset=1):
    """Task to generate an invoice for a specialist's sessions"""
    return Task(
        description=f"""
        Generate a complete invoice for specialist '{specialist_name}' 
        for the week {week_offset} week(s) ago.
        
        Steps:
        1. Use the schedule data from the previous task (if available)
        2. Read pricing information from {pricing_file}
        3. Filter sessions for the specified week only
        4. Calculate costs for each session based on type:
           - Match session types to pricing
           - Handle both "1 on 1" and "Group" sessions
        5. Generate itemized invoice including:
           - Invoice number and date
           - Billing period
           - Detailed session list with dates, clients, and costs
           - Summary by session type
           - Total amount due
        6. Use the template from {template_file} if available
        7. Format professionally
        
        Ensure all calculations are accurate.
        Include all billable sessions from the specified week.
        """,
        agent=agent,
        expected_output="Complete formatted invoice ready for sending",
        context=["extract_schedule_task"]  # This task depends on schedule extraction
    )

def batch_invoice_task(agent, specialists_list, pricing_file, template_file, week_offset=1):
    """Task to generate invoices for multiple specialists"""
    return Task(
        description=f"""
        Generate invoices for all specialists in the list: {specialists_list}
        for the week {week_offset} week(s) ago.
        
        Steps:
        1. For each specialist in the list:
           - Extract their sessions for the specified week
           - Calculate costs based on {pricing_file}
           - Generate individual invoice
        2. Create separate invoice files for each specialist
        3. Provide a summary report including:
           - Total revenue across all specialists
           - Session count breakdown
           - Highest and lowest billing specialists
        4. Flag any specialists with no sessions
        
        Maintain consistency across all invoices.
        Use the same template and formatting.
        """,
        agent=agent,
        expected_output="Multiple invoices and summary report"
    )

def invoice_validation_task(agent, invoice_data, pricing_file):
    """Task to validate invoice calculations"""
    return Task(
        description=f"""
        Validate the invoice calculations and data integrity.
        
        Steps:
        1. Review the invoice data: {invoice_data}
        2. Verify pricing against {pricing_file}
        3. Check for:
           - Correct price application for each session type
           - Accurate total calculations
           - Proper date range (correct week)
           - No missing sessions
           - No duplicate entries
        4. Recalculate totals independently
        5. Flag any discrepancies
        6. Suggest corrections if needed
        
        Be meticulous in validation.
        Ensure 100% accuracy in billing.
        """,
        agent=agent,
        expected_output="Validation report with any issues and corrections"
    )

def payment_tracking_task(agent, invoice_number, payment_status):
    """Task to track and update payment status"""
    return Task(
        description=f"""
        Update payment tracking for invoice {invoice_number}.
        
        Steps:
        1. Record payment status: {payment_status}
        2. Update payment tracking file
        3. Calculate:
           - Outstanding balance
           - Payment date (if paid)
           - Days overdue (if applicable)
        4. Generate payment status report
        5. If overdue, prepare reminder notice
        
        Maintain accurate payment records.
        """,
        agent=agent,
        expected_output="Payment status update and any necessary follow-up actions"
    )

def monthly_billing_summary_task(agent, pricing_file, month=None):
    """Task to generate monthly billing summary"""
    return Task(
        description=f"""
        Generate a comprehensive monthly billing summary for {month or 'current month'}.
        
        Steps:
        1. Compile all invoices for the month
        2. Calculate:
           - Total revenue
           - Revenue by specialist
           - Revenue by session type
           - Average session value
           - Client frequency analysis
        3. Compare to previous month (if data available)
        4. Identify trends:
           - Growing/declining session types
           - Specialist utilization
           - Client retention
        5. Generate visual summary (text-based charts)
        6. Provide recommendations for optimization
        
        Create executive-level summary with key insights.
        """,
        agent=agent,
        expected_output="Comprehensive monthly billing report with analytics"
    )

def client_billing_history_task(agent, client_name, date_range=None):
    """Task to generate billing history for a specific client"""
    return Task(
        description=f"""
        Generate complete billing history for client '{client_name}'.
        
        Steps:
        1. Search all invoices for sessions with {client_name}
        2. Compile history including:
           - All sessions attended
           - Dates and specialists
           - Session types
           - Total amount billed
        3. Calculate:
           - Total sessions
           - Total cost
           - Average session frequency
           - Preferred specialists
        4. Include date range: {date_range or 'all available'}
        5. Format as client statement
        
        Provide comprehensive client billing overview.
        """,
        agent=agent,
        expected_output="Complete billing history for the specified client"
    )
