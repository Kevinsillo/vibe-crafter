# Python - Microservicio (Nivel 2)

> Solo leer si el tipo de proyecto es Microservicio.

## Librerias recomendadas

- **FastAPI:** framework web async
- **uvicorn:** servidor ASGI
- **pydantic-settings:** configuracion tipada desde env vars
- **structlog:** logging estructurado (JSON)
- **httpx:** cliente HTTP async para comunicacion entre servicios
- **tenacity:** reintentos con backoff

## Estructura

Igual que API REST pero con estos extras:

```
src/nombre_proyecto/
  infrastructure/
    config/
      settings.py        # pydantic-settings
    health/
      health_controller.py
    clients/
      other_service_client.py  # adaptador HTTP a otro servicio
```

## Health check obligatorio

```python
@router.get("/health")
def health():
    return {"status": "ok"}
```

Todo microservicio debe exponer `/health` para orquestadores (Docker, K8s).

## Configuracion via entorno

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    service_name: str = "mi-servicio"
    debug: bool = False

    class Config:
        env_file = ".env"
```

## Comunicacion entre servicios

Los clientes HTTP a otros servicios son adaptadores de salida:

```python
class OrderServiceClient(OrderServicePort):
    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url)

    async def get_order(self, order_id: str) -> Order:
        response = await self._client.get(f"/orders/{order_id}")
        response.raise_for_status()
        return Order.from_dict(response.json())
```

## Reglas

- Cada microservicio tiene un unico dominio acotado (bounded context).
- Logging estructurado siempre (no print).
- Configuracion por variables de entorno, nunca hardcoded.
- Health check obligatorio.
- Timeouts y reintentos en clientes HTTP.
- Docker-ready: incluir Dockerfile minimo.
