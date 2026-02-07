# VibeCrafter

Plantilla de proyecto que guia a agentes de IA (Claude Code, Cursor, Copilot, etc.) para generar codigo con arquitectura hexagonal de forma estructurada y profesional.

## El problema

El vibe coding sin estructura produce codigo desorganizado: arquitectura superficial, patrones mal aplicados y logica de negocio mezclada con infraestructura. Los agentes de IA tienden a improvisar si no se les da contexto tecnico previo.

## La solucion

VibeCrafter es un sistema de **instrucciones jerarquicas** que fuerza al agente a adquirir conocimiento arquitectonico antes de generar codigo. El usuario solo describe *que* quiere construir; la arquitectura emerge del sistema.

### Como funciona

1. **El usuario ejecuta un asistente interactivo** que recoge los datos del proyecto (nombre, tipo, lenguaje, dependencias).
2. **Se genera un fichero `project.md`** con los datos del usuario y las instrucciones para el agente.
3. **El agente sigue 8 fases obligatorias** antes de escribir una sola linea de codigo: carga de conocimiento, diseno conceptual, creacion de estructura y generacion guiada.

## Inicio rapido

```bash
# Clona el repositorio
git clone <url-del-repo> mi-proyecto
cd mi-proyecto

# Ejecuta el asistente
bash .vibecrafter/iniciar.sh

# Abre project.md con tu agente de IA y pidele que lo lea
```

## Fases del agente

| Fase | Nombre | Descripcion |
|------|--------|-------------|
| 0 | Lectura del formulario | Comprende los requisitos del usuario |
| 1 | Conocimiento obligatorio | Lee hexagonal, buenas practicas y testing |
| 2 | Conocimiento por lenguaje | Carga convenciones del lenguaje elegido |
| 3 | Carga condicional | Lee docs de tipo de proyecto, persistencia, auth, diseno |
| 4 | Diseno conceptual | Define entidades, casos de uso y estructura |
| 5 | Creacion de estructura | Genera carpetas y ficheros vacios |
| 6 | Generacion de codigo | Implementa dominio, aplicacion, infra y tests |
| 7 | Revision | Autoevaluacion con checklist de reglas |

## Lenguajes soportados

- **Python** (completo)
- ~~TypeScript~~ (pendiente)

## Contribuir

El proyecto esta preparado para crecer:

- **Nuevo lenguaje:** crea una carpeta en `languages/` con `conventions.md` y `testing.md`.
- **Nuevo tipo de proyecto:** anade un `.md` en `languages/[lang]/project_types/`.
- **Nuevo diseno:** anade un `.md` en `designs/`. El asistente lo detecta automaticamente.

## Licencia

GPL-3.0 License. Libre para uso personal y comercial, con atribucion al autor.
