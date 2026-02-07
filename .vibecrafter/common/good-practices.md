# Buenas Practicas - Reglas transversales

## Principios SOLID (aplicar siempre)

- **S** - Responsabilidad unica: cada clase/funcion hace una sola cosa.
- **O** - Abierto/cerrado: extender comportamiento sin modificar codigo existente.
- **L** - Sustitucion de Liskov: las implementaciones deben ser intercambiables.
- **I** - Segregacion de interfaces: interfaces pequenas y especificas.
- **D** - Inversion de dependencias: depender de abstracciones, no de implementaciones.

## Nombrado

- Nombres descriptivos. Evitar abreviaturas ambiguas.
- Casos de uso: verbo + sustantivo (`CreateUser`, `GetOrderById`).
- Puertos: describir capacidad (`UserRepository`, `EmailSender`).
- Entidades: sustantivo del dominio (`Order`, `Product`, `User`).

## Manejo de errores

- Usar excepciones de dominio especificas, no excepciones genericas.
- La capa de aplicacion atrapa excepciones de dominio y las transforma.
- La infraestructura nunca lanza excepciones de dominio directamente.
- Patron: `DomainException` -> `ApplicationException` -> respuesta HTTP/CLI.

## Inmutabilidad y validacion

- Los Value Objects son inmutables y se validan en construccion.
- Las entidades validan sus invariantes internamente.
- No permitir estados invalidos. Fallar rapido.

## Inyeccion de dependencias

- Siempre inyectar dependencias por constructor.
- No usar singletons ni estado global.
- La composicion se hace en la capa de infraestructura (composition root).

## Reglas de codigo

- Funciones cortas (max ~20 lineas como guia).
- Evitar anidacion profunda (max 2 niveles).
- No comentar codigo muerto: eliminarlo.
- No usar numeros magicos: extraer a constantes con nombre.
- DRY solo cuando la duplicacion es real, no especulativa.
