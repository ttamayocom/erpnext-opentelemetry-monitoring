# ERPNext OpenTelemetry Monitoring App

App de Frappe/ERPNext para instrumentación OpenTelemetry y métricas personalizadas.

## Propósito

- Instrumentación OpenTelemetry para observabilidad
- Hooks de eventos de documentos (after_insert, on_submit)
- Métricas personalizadas (documents_created, documents_submitted, sales_order_value)

## Creación del App (Método Oficial)

**IMPORTANTE**: Este app debe crearse usando el método oficial de Frappe Bench:

```bash
# En un bench de desarrollo local (con TTY interactivo)
cd /path/to/frappe-bench
bench new-app erpnext-opentelemetry-monitoring
# Responder a los prompts:
# - App Title: ERPNext OpenTelemetry Monitoring
# - App Description: OpenTelemetry instrumentation and custom metrics for ERPNext
# - App Publisher: Tu organización
# - App Email: tu@email.com
# - App License: MIT
```

Después de crear el app oficialmente, agregar los archivos de hooks y métricas:

1. **hooks.py**: Agregar doc_events para instrumentación
2. **otel_metrics.py**: SDK de OpenTelemetry para métricas
3. **metrics_hooks.py**: Hooks que llaman a las métricas

## Instalación en Producción

Una vez creado el app oficialmente y pusheado a este repositorio:

```bash
# En el bench de producción (vía Ansible/automation)
bench get-app erpnext-opentelemetry-monitoring https://github.com/ttamayo/erpnext-opentelemetry-monitoring
bench --site <site> install-app erpnext-opentelemetry-monitoring
```

## Configuración en tt-erpnext-automation

El app se configura en `terraform/config.yaml`:

```yaml
service:
  app:
    external_apps:
      - name: "erpnext-opentelemetry-monitoring"
        url: "https://github.com/ttamayo/erpnext-opentelemetry-monitoring"
    
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

## Notas

- El nombre del app usa guiones (`erpnext-opentelemetry-monitoring`) para el directorio
- El nombre del módulo Python usa guiones bajos (`erpnext_opentelemetry_monitoring`)
- Frappe Bench maneja esta conversión automáticamente
