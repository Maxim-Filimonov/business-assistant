"""
Invoice Tools for Billing and Invoice Generation
"""

from crewai.tools import BaseTool
from typing import List, Dict
from datetime import datetime, timedelta
import re

class PricingReader(BaseTool):
    name: str = "Pricing Reader"
    description: str = "Reads and parses pricing information from markdown"

    def _run(self, pricing_file: str) -> Dict[str, float]:
        """Read pricing information from markdown file"""
        try:
            with open(pricing_file, 'r', encoding='utf-8') as f:
                content = f.read()

            pricing = {}
            lines = content.split('\n')

            for line in lines:
                # Look for pricing patterns (e.g., "- 1 on 1 session - 50$")
                price_match = re.search(r'[-*]\s*(.+?)\s*[-–]\s*\$?(\d+)', line)
                if price_match:
                    session_type = price_match.group(1).strip()
                    price = float(price_match.group(2))
                    pricing[session_type.lower()] = price

            return pricing
        except Exception as e:
            return {'error': f"Error reading pricing: {str(e)}"}

class SessionCalculator(BaseTool):
    name: str = "Session Calculator"
    description: str = "Calculates total cost for sessions based on pricing"

    def _run(self, sessions: List[Dict], pricing: Dict[str, float]) -> Dict:
        """Calculate totals for sessions"""
        session_counts = {}
        session_details = []
        total = 0.0

        for session in sessions:
            session_type = session.get('type', '1 on 1 session')

            # Count sessions by type
            if session_type not in session_counts:
                session_counts[session_type] = 0
            session_counts[session_type] += 1

            # Find price
            price = 0.0
            for pricing_key, pricing_value in pricing.items():
                if session_type.lower() in pricing_key or pricing_key in session_type.lower():
                    price = pricing_value
                    break

            # Add to details
            session_details.append({
                'date': session['date'],
                'time': session['time'],
                'client': session['client'],
                'type': session_type,
                'price': price
            })

            total += price

        return {
            'session_counts': session_counts,
            'session_details': session_details,
            'total': total
        }

class InvoiceGenerator(BaseTool):
    name: str = "Invoice Generator"
    description: str = "Generates formatted invoices from templates"

    def _run(self, template_path: str, invoice_data: Dict, output_path: str = None) -> str:
        """Generate invoice from template"""
        try:
            # Read template
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            # Get current date and invoice period
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday() + 7)  # Last week start
            week_end = week_start + timedelta(days=6)

            # Prepare invoice data
            invoice_number = f"INV-{today.strftime('%Y%m%d')}-001"

            # Replace template placeholders
            replacements = {
                '{{INVOICE_NUMBER}}': invoice_number,
                '{{DATE}}': today.strftime('%B %d, %Y'),
                '{{PERIOD_START}}': week_start.strftime('%B %d, %Y'),
                '{{PERIOD_END}}': week_end.strftime('%B %d, %Y'),
                '{{SPECIALIST_NAME}}': invoice_data.get('specialist', 'N/A'),
                '{{TOTAL_AMOUNT}}': f"${invoice_data.get('total', 0):.2f}",
                '{{SESSION_DETAILS}}': self._format_sessions(invoice_data.get('session_details', [])),
                '{{SESSION_SUMMARY}}': self._format_summary(invoice_data.get('session_counts', {}))
            }

            invoice = template
            for placeholder, value in replacements.items():
                invoice = invoice.replace(placeholder, value)

            # Save invoice if output path provided
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(invoice)
                return f"Invoice generated and saved to {output_path}"

            return invoice

        except Exception as e:
            return f"Error generating invoice: {str(e)}"

    def _format_sessions(self, sessions: List[Dict]) -> str:
        """Format session details for invoice"""
        if not sessions:
            return "No sessions recorded"

        formatted = []
        for session in sessions:
            line = f"- {session['date']} at {session['time']} - {session['client']} ({session['type']}) - ${session['price']:.2f}"
            formatted.append(line)

        return '\n'.join(formatted)

    def _format_summary(self, counts: Dict) -> str:
        """Format session summary"""
        if not counts:
            return "No sessions"

        summary = []
        for session_type, count in counts.items():
            summary.append(f"- {session_type}: {count} session(s)")

        return '\n'.join(summary)

class InvoiceTemplateCreator(BaseTool):
    name: str = "Invoice Template Creator"
    description: str = "Creates invoice templates"

    def _run(self, specialist_name: str = None) -> str:
        """Create a basic invoice template"""
        template = """# INVOICE

**Invoice Number:** {{INVOICE_NUMBER}}
**Date:** {{DATE}}
**Billing Period:** {{PERIOD_START}} to {{PERIOD_END}}

---

## Specialist Information
**Name:** {{SPECIALIST_NAME}}

---

## Session Details

{{SESSION_DETAILS}}

---

## Summary

{{SESSION_SUMMARY}}

---

## Total Amount Due

**{{TOTAL_AMOUNT}}**

---

*Payment due within 30 days*
*Thank you for your business!*
"""
        return template
