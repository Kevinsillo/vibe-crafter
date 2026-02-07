# Python - Persistencia (Nivel 2)

> Solo leer si el proyecto usa base de datos.

## Principio

El dominio NO sabe que existe una base de datos. La persistencia es un detalle de infraestructura.

## Puerto de salida (aplicacion)

```python
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_id(self, user_id: UserId) -> User | None: ...

    @abstractmethod
    def find_all(self) -> list[User]: ...
```

## Adaptador (infraestructura)

### SQLAlchemy (SQL)

- Usar modelos ORM separados de las entidades de dominio.
- Crear mappers/converters entre modelo ORM y entidad de dominio.
- No exponer modelos ORM fuera de infraestructura.

```python
class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, user: User) -> None:
        model = UserModel.from_entity(user)
        self._session.add(model)
        self._session.commit()

    def find_by_id(self, user_id: UserId) -> User | None:
        model = self._session.get(UserModel, str(user_id.value))
        return model.to_entity() if model else None
```

### MongoDB

- Usar `pymongo` o `motor` (async).
- Serializar entidades a dict para almacenar.
- Mismo patron: puerto en aplicacion, adaptador en infraestructura.

## Migraciones

- Usar `alembic` para SQL.
- Mantener migraciones en `infrastructure/persistence/migrations/`.

## Anti-patrones a evitar

- Entidades que heredan de `Base` del ORM.
- Repositorios que devuelven modelos ORM.
- Logica de negocio en queries SQL.
