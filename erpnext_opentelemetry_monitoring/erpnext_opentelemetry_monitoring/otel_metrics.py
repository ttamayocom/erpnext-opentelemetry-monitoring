# OpenTelemetry Metrics SDK for ERPNext
# Initializes OpenTelemetry Metrics SDK and creates business metrics instruments

import os
import logging
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

logger = logging.getLogger(__name__)

def init_metrics():
    """
    Initialize OpenTelemetry Metrics SDK for ERPNext.
    
    Returns:
        MeterProvider instance or None if initialization fails (graceful degradation)
    """
    try:
        # Resource attributes (from environment variables set by wrapper scripts)
        resource = Resource.create({
            SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "erpnext"),
            "deployment.environment": os.getenv("DEPLOYMENT_ENV", "production"),
            "service.version": os.getenv("OTEL_SERVICE_VERSION", "unknown"),
        })
        
        # Parse headers from environment variable
        headers = {}
        otel_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")
        if otel_headers:
            for header in otel_headers.split(','):
                if '=' in header:
                    key, value = header.strip().split('=', 1)
                    headers[key] = value
        
        # OTLP Metric Exporter
        # CRITICAL: Use OTEL_EXPORTER_OTLP_METRICS_ENDPOINT from wrapper scripts
        exporter = OTLPMetricExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT", "http://localhost:4318/v1/metrics"),
            headers=headers if headers else None,
        )
        
        # Periodic Exporting Metric Reader (exports every 60 seconds)
        reader = PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=60000,  # 60 seconds
        )
        
        # Meter Provider
        provider = MeterProvider(resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(provider)
        
        logger.info("OpenTelemetry Metrics SDK initialized successfully")
        return provider
    except Exception as e:
        logger.error(f"Failed to initialize OTEL metrics: {e}")
        return None  # Graceful degradation - metrics disabled, app continues

# Initialize metrics provider (called on app startup)
_metrics_provider = init_metrics()

# Create meter for business metrics
meter = metrics.get_meter("erpnext.business", "1.0.0")

# Business metrics instruments
documents_created = meter.create_counter(
    name="erpnext.documents.created.total",
    description="Total documents created in ERPNext",
    unit="1"
)

documents_submitted = meter.create_counter(
    name="erpnext.documents.submitted.total", 
    description="Total documents submitted in ERPNext",
    unit="1"
)

sales_order_value = meter.create_histogram(
    name="erpnext.sales_order.value",
    description="Sales order value distribution",
    unit="USD"
)

# Initialize metrics on module import (called when app loads)
# This ensures metrics are available when hooks are called
if _metrics_provider is not None:
    logger.info("OpenTelemetry Metrics SDK initialized - business metrics available")
else:
    logger.warning("OpenTelemetry Metrics SDK initialization failed - business metrics disabled")

