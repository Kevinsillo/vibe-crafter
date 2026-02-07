# Python - API REST (Nivel 2)

> Solo leer si el proyecto es una API REST.

## Framework recomendado

- **FastAPI** (preferido): async, type hints, OpenAPI automatico.
- **Flask**: si el proyecto es simple y sincrono.

## Controladores como adaptadores de entrada

Los controladores viven en `infrastructure/adapters/input/api/`. Son adaptadores que:
1. Reciben la peticion HTTP.
2. Transforman a un comando/query de aplicacion.
3. Invocan el caso de uso.
4. Transforman la respuesta del dominio a HTTP.

```python
# infrastructure/adapters/input/api/user_controller.py
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=201)
def create_user(
    request: CreateUserRequest,
    use_case: CreateUser = Depends(get_create_user),
):
    try:
        user_id = use_case.execute(
            CreateUserCommand(name=request.name, email=request.email)
        )
        return {"id": str(user_id.value)}
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## DTOs / Schemas

- Usar Pydantic models para request/response.
- Separar schemas de entrada y salida.
- Los schemas viven junto al controlador, NO en dominio.

```python
class CreateUserRequest(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
```

## Manejo de errores

- Crear un exception handler global que mapee excepciones de dominio a codigos HTTP.
- 400: error de validacion/dominio.
- 404: recurso no encontrado.
- 500: error inesperado (loguear, no exponer detalles).

## Estructura

```
infrastructure/adapters/input/api/
  __init__.py
  user_controller.py
  schemas/
    user_schemas.py
  error_handler.py
  app.py  (composicion de la app FastAPI)
```

## Anti-patrones a evitar

- Logica de negocio en el controlador.
- Controlador que accede directamente al repositorio.
- Schemas de Pydantic usados como entidades de dominio.
