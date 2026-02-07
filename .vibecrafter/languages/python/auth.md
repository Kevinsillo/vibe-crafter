# Python - Autenticacion (Nivel 2)

> Solo leer si el proyecto usa autenticacion.

## Principio

La autenticacion es infraestructura. El dominio no sabe como se autentica un usuario.

## Puerto de salida

```python
class AuthService(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> AuthenticatedUser: ...

    @abstractmethod
    def generate_token(self, user: User) -> str: ...
```

## JWT - Adaptador

```python
class JWTAuthService(AuthService):
    def __init__(self, secret: str, algorithm: str = "HS256") -> None:
        self._secret = secret
        self._algorithm = algorithm

    def generate_token(self, user: User) -> str:
        payload = {"sub": str(user.id.value), "exp": datetime.utcnow() + timedelta(hours=1)}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def verify_token(self, token: str) -> AuthenticatedUser:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return AuthenticatedUser(user_id=UserId(payload["sub"]))
        except jwt.InvalidTokenError:
            raise InvalidCredentials()
```

## Middleware / Dependency (FastAPI)

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth: AuthService = Depends(get_auth_service),
) -> AuthenticatedUser:
    return auth.verify_token(token)
```

## Reglas

- El token se valida en infraestructura, no en dominio.
- Los casos de uso reciben un `AuthenticatedUser`, no un token.
- No guardar secretos en codigo: usar variables de entorno.
- `InvalidCredentials` es una excepcion de dominio.

## Estructura

```
domain/value_objects/authenticated_user.py
application/ports/output/auth_service.py
infrastructure/adapters/output/auth/jwt_auth_service.py
```
