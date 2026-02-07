# Testing - Estrategia obligatoria

## Principio

El testing no es opcional. Cada caso de uso debe tener test antes de pasar al siguiente. El testing guia el diseno, no lo complementa.

## Piramide de tests por capa

### Dominio - Tests unitarios puros
- Sin mocks, sin dependencias externas.
- Testear logica de entidades y value objects.
- Validar invariantes y reglas de negocio.
- Ejemplo: `test_order_cannot_have_negative_quantity`

### Aplicacion - Tests unitarios con mocks
- Mockear los puertos de salida (driven ports).
- Testear que el caso de uso orquesta correctamente.
- Verificar que se llaman los puertos esperados.
- Ejemplo: `test_create_user_calls_repository_and_sends_email`

### Infraestructura - Tests de integracion
- Testear adaptadores contra servicios reales (o contenedores).
- Repositorios contra base de datos real/in-memory.
- Controladores con peticiones HTTP reales.
- Aislados: cada test limpia su estado.

## Reglas obligatorias

1. Cada caso de uso -> al menos 1 test happy path + 1 test error.
2. Cada entidad con logica -> tests de sus invariantes.
3. Cada value object -> test de validacion y test de igualdad.
4. No testear implementaciones internas, testear comportamiento.
5. Los tests deben poder ejecutarse sin infraestructura externa (salvo integracion).

## Nombrado de tests

Patron: `test_[accion]_[condicion]_[resultado_esperado]`

Ejemplos:
- `test_create_order_with_valid_data_returns_order`
- `test_create_order_with_empty_items_raises_error`

## Estructura de carpetas de tests

```
tests/
  domain/
  application/
  infrastructure/
```

Espejo de la estructura `src/`. Cada modulo tiene su carpeta de tests correspondiente.
