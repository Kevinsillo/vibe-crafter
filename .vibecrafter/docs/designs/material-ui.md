# Diseno Visual - Material Design

## Filosofia

Diseno basado en superficies, elevacion y movimiento. Jerarquia visual clara mediante sombras, color y tipografia. Componentes reconocibles y accesibles.

## Paleta de colores

| Rol              | Valor       |
|------------------|-------------|
| Primary          | `#1976D2`   |
| Primary dark     | `#1565C0`   |
| Primary light    | `#42A5F5`   |
| Secondary        | `#9C27B0`   |
| Fondo            | `#FAFAFA`   |
| Surface          | `#FFFFFF`   |
| Error            | `#D32F2F`   |
| Success          | `#2E7D32`   |
| Warning          | `#ED6C02`   |
| Texto principal  | `rgba(0,0,0,0.87)` |
| Texto secundario | `rgba(0,0,0,0.60)` |

## Tipografia

- **Principal:** `Roboto` (sans-serif)
- **Monoespaciada:** `Roboto Mono`
- **Escala tipografica:**
  - h1: 96px / light
  - h2: 60px / light
  - h3: 48px / regular
  - h4: 34px / regular
  - h5: 24px / regular
  - h6: 20px / medium
  - body1: 16px / regular
  - body2: 14px / regular
  - caption: 12px / regular

## Elevacion (sombras)

- Nivel 0: sin sombra (elementos planos)
- Nivel 1: `0 1px 3px rgba(0,0,0,0.12)` (cards en reposo)
- Nivel 2: `0 3px 6px rgba(0,0,0,0.16)` (cards hover, dropdowns)
- Nivel 3: `0 10px 20px rgba(0,0,0,0.19)` (modales, dialogs)

## Componentes clave

### Botones
- Contained: fondo primary, texto blanco, border-radius 4px, elevacion nivel 1
- Outlined: borde primary, fondo transparente
- Text: sin borde ni fondo, solo color primary
- Uppercase en labels, letter-spacing 0.5px
- Ripple effect en interaccion

### Cards
- Fondo blanco, border-radius 4px, elevacion nivel 1
- Padding 16px
- Hover: elevacion nivel 2

### Navegacion
- AppBar superior: fondo primary, elevacion nivel 2
- Drawer lateral para navegacion secundaria
- Bottom navigation en mobile

### Formularios
- Inputs con linea inferior (outlined o filled)
- Labels flotantes que suben al hacer focus
- Helper text debajo, error text en rojo
- Border-radius 4px (variant outlined)

### Tablas
- Data tables con header destacado
- Checkbox para seleccion
- Paginacion integrada
- Sorting por columnas

## Espaciado

- Sistema de 8px: 8, 16, 24, 32, 40, 48, 56, 64
- Padding interno: 16px (compacto), 24px (normal)
- Margenes entre secciones: 32-48px

## Responsive / Mobile first

- Mobile: 1 columna, bottom navigation, drawer lateral
- Tablet (600px): 2 columnas, navigation rail
- Desktop (960px+): layout completo, drawer permanente
- Breakpoints: 600px, 960px, 1280px, 1920px

## Reglas generales

- Border-radius consistente: 4px (botones/inputs), 8px (cards), 16px (modales)
- Transiciones: `transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1)`
- Iconos: Material Icons o Material Symbols (outlined)
- Usar elevacion para jerarquia, no bordes
- FAB (Floating Action Button) para la accion principal en mobile
