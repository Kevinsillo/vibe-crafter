# Python - Web App (Nivel 2)

> Solo leer si el tipo de proyecto es Web app.

## Enfoque

La web app es mobile first y responsive por defecto. El frontend puede ser:
- **Motor de plantillas:** HTML renderizado en servidor (Jinja2). Mas simple, ideal para apps internas o CRUD.
- **Frontend separado:** SPA con framework JS (React, Vue, etc.) que consume la API. Mas complejo, ideal para UX rica.

El formulario del proyecto indica cual se ha elegido.

## Librerias recomendadas

### Con motor de plantillas (server-side rendering)
- **FastAPI + Jinja2:** framework web + motor de plantillas
- **python-multipart:** procesamiento de formularios
- **htmx:** interactividad sin escribir JS (opcional pero recomendado)
- **TailwindCSS (via CDN o standalone):** estilos utility-first

### Con frontend separado
- **FastAPI:** API backend
- **CORS middleware:** `fastapi.middleware.cors`
- El frontend es un proyecto separado (no se genera en este sistema)

### Comunes
- **uvicorn:** servidor ASGI
- **python-dotenv:** variables de entorno
- **staticfiles:** servir archivos estaticos

## Estructura con motor de plantillas

```
src/
  nombre_proyecto/
    api/
      app.py
      routes/
      templates/
        base.html
        pages/
        components/
      static/
        css/
        js/
        img/
```

## Reglas

- Aplicar el documento de diseno seleccionado (`.vibecrafter/designs/[diseno].md`).
- Mobile first: disenar para movil, escalar a desktop (mientras no se especifique lo contrario).
- Las templates NO contienen logica de negocio.
- Los routes llaman a casos de uso, nunca acceden a repositorios directamente.
- Separar layouts (base.html) de paginas y componentes reutilizables.
