# Diseno Visual - Estilo Vercel

## Filosofia

Minimalismo funcional. Espacios amplios, tipografia limpia, interfaz sin ruido visual. Prioridad a la legibilidad y la velocidad percibida.

## Paleta de colores

| Rol              | Claro       | Oscuro      |
|------------------|-------------|-------------|
| Fondo            | `#FFFFFF`   | `#000000`   |
| Fondo secundario | `#FAFAFA`   | `#111111`   |
| Texto principal  | `#171717`   | `#EDEDED`   |
| Texto secundario | `#666666`   | `#888888`   |
| Borde            | `#EAEAEA`   | `#333333`   |
| Acento           | `#0070F3`   | `#0070F3`   |
| Exito            | `#0070F3`   | `#0070F3`   |
| Error            | `#EE0000`   | `#FF4444`   |
| Warning          | `#F5A623`   | `#F5A623`   |

## Tipografia

- **Principal:** `Inter` (sans-serif)
- **Monoespaciada:** `JetBrains Mono` o `Fira Code`
- **Tamanos:** 14px base, 13px secundario, 24-32px titulos
- **Peso:** 400 regular, 500 medium, 600 semibold

## Componentes clave

### Botones
- Primario: fondo negro, texto blanco, border-radius 6px
- Secundario: fondo transparente, borde gris, texto negro
- Hover: ligera elevacion o cambio de opacidad
- Sin sombras agresivas

### Cards
- Fondo blanco, borde 1px `#EAEAEA`, border-radius 8px
- Padding 24px
- Sin sombra o sombra muy sutil (`0 2px 4px rgba(0,0,0,0.05)`)

### Navegacion
- Barra superior fija, fondo blanco/negro con blur
- Links simples, sin iconos decorativos innecesarios
- Breadcrumbs con separador `/`

### Formularios
- Inputs con borde fino, border-radius 6px, padding 8px 12px
- Labels encima del input, no flotantes
- Validacion inline, mensajes de error en rojo debajo

### Tablas
- Bordes horizontales unicamente
- Header en gris claro
- Filas alternas sin color (usar hover sutil)

## Espaciado

- Sistema de 4px: 4, 8, 12, 16, 24, 32, 48, 64
- Margenes entre secciones: 48-64px
- Padding interno de contenedores: 24-32px

## Responsive / Mobile first

- Mobile: 1 columna, navegacion hamburguesa
- Tablet (768px): 2 columnas donde aplique
- Desktop (1024px+): layout completo, max-width 1200px centrado
- Breakpoints: 640px, 768px, 1024px, 1280px

## Reglas generales

- Dark mode como opcion, no obligatorio (implementar si el usuario lo pide)
- Transiciones suaves: `transition: all 150ms ease`
- Iconos: Lucide o Heroicons (outline)
- Sin gradientes, sin sombras dramaticas, sin bordes redondeados excesivos
