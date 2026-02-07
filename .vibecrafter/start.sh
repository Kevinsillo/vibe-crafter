#!/usr/bin/env bash
set -euo pipefail

# ─── Colores ────────────────────────────────────────────────
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
RESET='\033[0m'

# ─── Variables del formulario ───────────────────────────────
NOMBRE=""
DESC_BREVE=""
DESC_DETALLADA=""
TIPO_PROYECTO=""
WEBAPP_FRONTEND=""
LENGUAJE=""
BASE_DATOS=""
AUTH=""
TESTING=""
DISENO=""
NOTAS=""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_FILE="$PROJECT_DIR/project.md"

VIBECRAFTER_DIR="$SCRIPT_DIR"
DESIGNS_DIR="$VIBECRAFTER_DIR/designs"
INSTRUCCIONES_FILE="$VIBECRAFTER_DIR/instructions.md"

PASO_ACTUAL=0

# ─── Funciones auxiliares ───────────────────────────────────

print_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}║    Generador de Proyecto - Arquitectura Hexagonal    ║${RESET}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${RESET}"
    echo ""
}

print_step() {
    echo -e "${YELLOW}▸ $1${RESET}"
    echo ""
}

next_step() {
    PASO_ACTUAL=$((PASO_ACTUAL + 1))
}

select_option() {
    local prompt="$1"
    shift
    local options=("$@")

    echo -e "${BOLD}$prompt${RESET}"
    echo ""
    for i in "${!options[@]}"; do
        echo -e "  ${GREEN}$((i + 1)))${RESET} ${options[$i]}"
    done
    echo ""

    while true; do
        read -rp "  Selecciona [1-${#options[@]}]: " choice
        if [[ "$choice" =~ ^[0-9]+$ ]] && ((choice >= 1 && choice <= ${#options[@]})); then
            SELECTED="${options[$((choice - 1))]}"
            return
        fi
        echo -e "  ${RED}Opcion no valida. Intenta de nuevo.${RESET}"
    done
}

read_input() {
    local prompt="$1"
    local var_name="$2"

    echo -e "${BOLD}$prompt${RESET}"
    echo ""
    read -rp "  > " input_value
    eval "$var_name=\"\$input_value\""
    echo ""
}

read_multiline() {
    local prompt="$1"
    local var_name="$2"

    echo -e "${BOLD}$prompt${RESET}"
    echo -e "  (Escribe las funcionalidades. Linea vacia para terminar)"
    echo ""

    local lines=""
    while true; do
        read -rp "  > " line
        [[ -z "$line" ]] && break
        lines+="  - $line"$'\n'
    done
    eval "$var_name=\"\$lines\""
}

necesita_diseno() {
    [[ "$TIPO_PROYECTO" == "Web app" || "$TIPO_PROYECTO" == "CLI" ]]
}

listar_disenos() {
    local designs=()
    if [[ -d "$DESIGNS_DIR" ]]; then
        for f in "$DESIGNS_DIR"/*.md; do
            [[ -f "$f" ]] || continue
            local name
            name=$(basename "$f" .md)
            designs+=("$name")
        done
    fi
    echo "${designs[@]}"
}

# ─── Flujo principal ────────────────────────────────────────

print_header
echo -e "  Este asistente te guiara para definir tu proyecto."
echo -e "  Al finalizar se generara ${BOLD}project.md${RESET} con toda la informacion."
echo ""
read -rp "  Pulsa Enter para comenzar..."

# --- Paso 1: Nombre + Descripcion breve ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Datos del proyecto"
read_input "Nombre del proyecto:" NOMBRE
read_input "Descripcion breve (1-2 frases):" DESC_BREVE

# --- Paso 2: Funcionalidades ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Funcionalidades"
read_multiline "Lista las funcionalidades principales:" DESC_DETALLADA

# --- Paso 3: Tipo de proyecto ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Tipo de proyecto"
select_option "Que tipo de proyecto es?" \
    "API REST" \
    "CLI" \
    "Web app" \
    "Microservicio" \
    "Libreria"
TIPO_PROYECTO="$SELECTED"

# --- Paso 3b: Sub-pregunta webapp ---
if [[ "$TIPO_PROYECTO" == "Web app" ]]; then
    echo ""
    select_option "Como quieres el frontend?" \
        "Motor de plantillas HTML (server-side, mas simple)" \
        "Frontend separado (SPA con React, Vue, etc.)"
    WEBAPP_FRONTEND="$SELECTED"
fi

# --- Paso 4: Lenguaje ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Lenguaje de programacion"
select_option "Que lenguaje quieres usar?" \
    "Python" \
    "TypeScript" \
    "Java" \
    "Go"
LENGUAJE="$SELECTED"

# --- Paso 5: Base de datos ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Base de datos"
select_option "Necesitas base de datos?" \
    "PostgreSQL" \
    "MySQL" \
    "MongoDB" \
    "SQLite" \
    "Ninguna"
BASE_DATOS="$SELECTED"

# --- Paso 6: Autenticacion ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Autenticacion"
select_option "Necesitas autenticacion?" \
    "No" \
    "JWT" \
    "OAuth2" \
    "Session"
AUTH="$SELECTED"

# --- Paso 7: Testing ---
print_header
next_step
print_step "Paso $PASO_ACTUAL - Testing"
select_option "Que tipo de testing quieres?" \
    "Unitarios" \
    "Integracion" \
    "Unitarios + Integracion" \
    "E2E" \
    "Ninguno"
TESTING="$SELECTED"

# --- Paso condicional: Diseno visual ---
if necesita_diseno; then
    print_header
    next_step
    print_step "Paso $PASO_ACTUAL - Diseno visual"

    read -ra designs_list <<< "$(listar_disenos)"

    if [[ ${#designs_list[@]} -gt 0 ]]; then
        select_option "Que estilo de diseno quieres aplicar?" \
            "${designs_list[@]}" \
            "Ninguno"
        DISENO="$SELECTED"
        if [[ "$DISENO" == "Ninguno" ]]; then
            DISENO=""
        fi
    else
        echo -e "  ${YELLOW}No se encontraron disenos en .vibecrafter/designs/${RESET}"
        DISENO=""
    fi
fi

# --- Notas extra ---
print_header
echo -e "${BOLD}Notas adicionales (opcional, Enter para saltar):${RESET}"
echo ""
read -rp "  > " NOTAS
echo ""

# ─── Secciones condicionales ────────────────────────────────

webapp_section=""
if [[ -n "$WEBAPP_FRONTEND" ]]; then
    webapp_section="- **Frontend:** $WEBAPP_FRONTEND"
fi

diseno_section=""
if [[ -n "$DISENO" ]]; then
    diseno_section="- **Diseno visual:** $DISENO"
fi

# ─── Generacion de proyecto.md ──────────────────────────────

cat > "$OUTPUT_FILE" << ENDOFFILE
# Proyecto: $NOMBRE

## 1. Datos del proyecto

- **Nombre del proyecto:** $NOMBRE
- **Descripcion breve:** $DESC_BREVE
- **Descripcion detallada / funcionalidades:**
$DESC_DETALLADA
- **Tipo de proyecto:** $TIPO_PROYECTO
${webapp_section:+$webapp_section
}- **Lenguaje de programacion:** $LENGUAJE

## 2. Contexto adicional

- **Base de datos:** $BASE_DATOS
- **Autenticacion:** $AUTH
- **Testing:** $TESTING
${diseno_section:+$diseno_section
}- **Notas extra:** ${NOTAS:-Ninguna}

---

ENDOFFILE

# Incluir el archivo de instrucciones del agente
if [[ -f "$INSTRUCCIONES_FILE" ]]; then
    cat "$INSTRUCCIONES_FILE" >> "$OUTPUT_FILE"
else
    echo "Error: No se encontró $INSTRUCCIONES_FILE" >&2
    exit 1
fi

# ─── Resultado ──────────────────────────────────────────────

print_header
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║          proyecto.md generado correctamente!         ║${RESET}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${BOLD}Resumen:${RESET}"
echo -e "  Proyecto:    $NOMBRE"
echo -e "  Tipo:        $TIPO_PROYECTO"
[[ -n "$WEBAPP_FRONTEND" ]] && echo -e "  Frontend:    $WEBAPP_FRONTEND"
echo -e "  Lenguaje:    $LENGUAJE"
echo -e "  Base datos:  $BASE_DATOS"
echo -e "  Auth:        $AUTH"
echo -e "  Testing:     $TESTING"
[[ -n "$DISENO" ]] && echo -e "  Diseno:      $DISENO"
echo ""
echo -e "  ${YELLOW}Siguiente paso:${RESET} Abre proyecto.md con tu agente de IA (Claude Code, Cursor, etc.)"
echo -e "  y pidele que lo lea para comenzar a construir tu proyecto."
echo ""
