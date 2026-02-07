# VibeCrafter

Sistema interactivo que genera instrucciones arquitectonicas para agentes de IA (Claude Code, Cursor, Copilot, etc.), guiandolos a producir codigo estructurado y profesional con arquitectura hexagonal.

## Motivacion

Soy un desarrollador apasionado por la programacion, meticuloso con las buenas practicas y con una debilidad por la arquitectura de software bien pensada. Creo que un buen proyecto no es solo el que funciona, sino el que se puede entender, mantener y escalar sin dolor.

Cuando el vibe coding empezo a ganar traccion, vi una oportunidad enorme: democratizar la creacion de software y permitir que cualquier persona con una idea pudiera materializarla. Pero tambien vi el riesgo.

## El problema

El vibe coding sin estructura produce codigo desorganizado: arquitectura superficial, patrones mal aplicados y logica de negocio mezclada con infraestructura. Los agentes de IA tienden a improvisar si no se les da contexto tecnico previo.

Quienes hemos trabajado con proyectos generados por vibe coding sin guia sabemos lo frustrante que es: codigo que funciona en la demo pero se desmorona al intentar extenderlo, sin separacion de capas, sin tests, con dependencias cruzadas por todas partes. Refactorizarlo suele costar mas que haberlo hecho bien desde el principio.

Y aqui esta la paradoja: el vibe coding es genial para prototipar rapido, pero sin una base arquitectonica solida, el prototipo se convierte en deuda tecnica desde el dia uno.

## La solucion

VibeCrafter es el punto medio entre el vibe coding y la programacion estructurada. No lucha contra la IA, la guia.

Es un sistema de **instrucciones jerarquicas** que fuerza al agente a adquirir conocimiento arquitectonico antes de generar codigo. El usuario solo describe *que* quiere construir; la arquitectura emerge del sistema de instrucciones.

El resultado es codigo generado por IA pero con la estructura, las convenciones y la calidad que esperarias de un proyecto hecho por un equipo senior.

### Como funciona

1. **El usuario ejecuta un asistente interactivo** que recoge los datos del proyecto (nombre, tipo, lenguaje, dependencias).
2. **Se genera un fichero `project.md`** con los datos del usuario y las instrucciones que el agente debe seguir.
3. **El agente sigue 7 fases obligatorias** (0-6) antes de escribir una sola linea de codigo: carga de conocimiento, diseno conceptual, creacion de estructura y generacion guiada.

Las fases estan definidas en las [instrucciones del generador](.vibecrafter/generator/instructions.md).

## Inicio rapido

```bash
# Clona el repositorio
git clone <url-del-repo> mi-proyecto
cd mi-proyecto

# Instala dependencias y ejecuta el asistente
cd .vibecrafter/generator
make install
make run

# Abre project.md con tu agente de IA y pidele que lo lea
```

## Lenguajes y disenos soportados

- **Lenguajes:** consulta los disponibles en [`.vibecrafter/docs/languages/`](.vibecrafter/docs/languages/)
- **Disenos visuales:** consulta los disponibles en [`.vibecrafter/docs/designs/`](.vibecrafter/docs/designs/)

El asistente detecta automaticamente los lenguajes, tipos de proyecto y disenos disponibles a partir de la estructura de carpetas.

## Contribuir

Este proyecto nace con vocacion de comunidad. La vision es que cualquier desarrollador pueda aportar sus convenciones, lenguajes o estilos de diseno para que mas personas se beneficien de un vibe coding con criterio.

Contribuir es tan sencillo como anadir un fichero `.md`:

- **Nuevo lenguaje:** crea una carpeta en [`docs/languages/`](.vibecrafter/docs/languages/) con `conventions.md` y `testing.md`.
- **Nuevo tipo de proyecto:** anade un `.md` en `docs/languages/[lenguaje]/project_types/`.
- **Nuevo diseno:** anade un `.md` en [`docs/designs/`](.vibecrafter/docs/designs/). El asistente lo detecta automaticamente.

## Licencia

GPL-3.0 License. Libre para uso personal y comercial, con atribucion al autor.
