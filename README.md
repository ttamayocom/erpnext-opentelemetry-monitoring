# ERPNext OpenTelemetry Monitoring App

App de Frappe/ERPNext para instrumentación OpenTelemetry y métricas personalizadas.

## Propósito

- Instrumentación OpenTelemetry para observabilidad
- Hooks de eventos de documentos (after_insert, on_submit)
- Métricas personalizadas (documents_created, documents_submitted, sales_order_value)

## Instalación

```bash
# En el bench de producción (vía Ansible/automation)
bench get-app erpnext-opentelemetry-monitoring https://github.com/ttamayocom/erpnext-opentelemetry-monitoring
bench --site <site> install-app erpnext-opentelemetry-monitoring
```

## Configuración en tt-erpnext-automation

El app se configura en `terraform/config.yaml`:

```yaml
service:
  app:
    external_apps:
      - name: "erpnext-opentelemetry-monitoring"
        url: "https://github.com/ttamayocom/erpnext-opentelemetry-monitoring"
    
    site_install_apps: ["erpnext", "education", "erpnext-opentelemetry-monitoring"]
```

## Estructura del App

```
erpnext-opentelemetry-monitoring/
├── pyproject.toml              # Configuración del paquete (generado por bench new-app)
├── erpnext_opentelemetry_monitoring/
│   ├── __init__.py             # Versión del app
│   ├── hooks.py                # Hooks de documentos (doc_events)
│   ├── modules.txt             # Módulos del app
│   ├── patches.txt            # Patches (vacío inicialmente)
│   └── erpnext_opentelemetry_monitoring/
│       ├── __init__.py         # Inicializador del módulo
│       ├── otel_metrics.py     # SDK de OpenTelemetry
│       └── metrics_hooks.py    # Hooks que llaman a métricas
```

## Métricas Disponibles

- `erpnext.documents.created.total` - Contador de documentos creados
- `erpnext.documents.submitted.total` - Contador de documentos enviados
- `erpnext.sales_order.value` - Histograma de valores de órdenes de venta

## Notas

- El nombre del app usa guiones (`erpnext-opentelemetry-monitoring`) para el directorio
- El nombre del módulo Python usa guiones bajos (`erpnext_opentelemetry_monitoring`)
- Frappe Bench maneja esta conversión automáticamente
- El app fue creado oficialmente con `bench new-app` en un entorno con TTY interactivo
