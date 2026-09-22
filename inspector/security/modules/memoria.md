# Memoria del Proyecto - E-Commerce Django

## Contexto Principal
- **Proyecto:** Marketplace e-commerce web en Django + Python.
- **Tecnologías:** Django Templates (HTML/CSS/JS), SQLite (local), PostgreSQL (producción), Firebase (Auth/Firestore) y PayPal.
- **Estructura del Proyecto:**
  - `unitux/`: Configuración global de Django (`settings.py`, `urls.py`).
  - `tienda/`: Lógica principal del marketplace (proveedores, productos, carritos, pagos, Firebase).
  - `usuarios/`: Registro y gestión de cuentas de usuario.
  - `.codex/`: Arquitectura de subagentes especializados (`codebase_mapper`, `django_backend`, `firebase_specialist`, etc.).

## Reglas de Trabajo
1. Responder siempre en **español**.
2. Mapear e inspeccionar el repositorio/código antes de modificarlo.
3. No cambiar la arquitectura ni romper la estructura modular sin diagnóstico previo.
4. Mantener respuestas claras, directas y enfocadas en código.

## Agentes Disponibles (.codex/agents/)
- `project_manager`
- `codebase_mapper`
- `architecture_reviewer`
- `django_backend`
- `frontend_engineer`
- `security_auditor`
- `database_architect`
- `payment_specialist`
- `firebase_specialist`
- `qa_engineer`
- `documentation_writer`