# Python - Mensajeria y Eventos (Nivel 2)

> Solo leer si el proyecto usa mensajeria o eventos.

## Principio

Los eventos de dominio nacen en el dominio. El transporte (RabbitMQ, Kafka, etc.) es infraestructura.

## Evento de dominio

```python
@dataclass(frozen=True)
class UserCreated:
    user_id: str
    email: str
    occurred_at: datetime
```

Los eventos son inmutables y representan hechos que ya ocurrieron.

## Puerto de salida

```python
class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None: ...
```

## Publicacion desde caso de uso

```python
class CreateUser:
    def __init__(self, repo: UserRepository, publisher: EventPublisher) -> None:
        self._repo = repo
        self._publisher = publisher

    def execute(self, command: CreateUserCommand) -> UserId:
        user = User.create(command.name, command.email)
        self._repo.save(user)
        self._publisher.publish(UserCreated(
            user_id=str(user.id.value),
            email=user.email.value,
            occurred_at=datetime.utcnow(),
        ))
        return user.id
```

## Adaptadores

### RabbitMQ
- Usar `pika` o `aio-pika` (async).
- Serializar eventos a JSON.

### Kafka
- Usar `confluent-kafka` o `aiokafka`.

### In-memory (para desarrollo/tests)
```python
class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)
```

## Reglas

- Los eventos se publican despues de la accion, no antes.
- Un evento no debe contener entidades completas, solo IDs y datos minimos.
- El consumidor de eventos es otro adaptador de entrada.
- Tests: usar `InMemoryEventPublisher` para verificar que se emiten los eventos correctos.

## Estructura

```
domain/events/user_created.py
application/ports/output/event_publisher.py
infrastructure/adapters/output/messaging/rabbitmq_publisher.py
infrastructure/adapters/input/messaging/user_event_consumer.py
```
