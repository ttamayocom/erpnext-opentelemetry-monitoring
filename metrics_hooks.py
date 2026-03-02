# OpenTelemetry Metrics Hooks for ERPNext
# Hooks that record business metrics when documents are created/submitted

import frappe
import logging

logger = logging.getLogger(__name__)

# Import metrics instruments (with graceful degradation if metrics not initialized)
try:
    from erpnext_opentelemetry_monitoring.erpnext_opentelemetry_monitoring.otel_metrics import (
        documents_created, documents_submitted, sales_order_value
    )
    METRICS_ENABLED = True
except ImportError as e:
    logger.warning(f"OpenTelemetry metrics not available: {e}")
    METRICS_ENABLED = False
    # Create dummy functions to prevent errors
    documents_created = None
    documents_submitted = None
    sales_order_value = None

def on_insert(doc, method):
    """Hook called when any document is inserted"""
    if not METRICS_ENABLED or documents_created is None:
        return
    
    try:
        documents_created.add(1, {
            "doctype": doc.doctype,
            "user": frappe.session.user if hasattr(frappe, 'session') else "system"
        })
    except Exception as e:
        logger.warning(f"Failed to record document created metric: {e}")

def on_submit(doc, method):
    """Hook called when any document is submitted"""
    if not METRICS_ENABLED or documents_submitted is None:
        return
    
    try:
        documents_submitted.add(1, {
            "doctype": doc.doctype,
            "user": frappe.session.user if hasattr(frappe, 'session') else "system"
        })
    except Exception as e:
        logger.warning(f"Failed to record document submitted metric: {e}")

def on_sales_order_submit(doc, method):
    """Hook called when Sales Order is submitted"""
    if not METRICS_ENABLED or sales_order_value is None:
        return
    
    try:
        # Record sales order value as histogram
        value = float(doc.grand_total) if hasattr(doc, 'grand_total') and doc.grand_total else 0.0
        sales_order_value.record(value, {
            "company": doc.company if hasattr(doc, 'company') else "unknown",
            "customer_group": doc.customer_group if hasattr(doc, 'customer_group') else "unknown"
        })
    except Exception as e:
        logger.warning(f"Failed to record sales order value metric: {e}")

