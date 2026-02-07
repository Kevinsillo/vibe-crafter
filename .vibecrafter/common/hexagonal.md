# Arquitectura Hexagonal - Reglas obligatorias

## Principio central

El dominio es el nucleo. No depende de nada externo. Todo lo demas depende del dominio.

## Capas y responsabilidades

```
[Infraestructura] --> [Aplicacion] --> [Dominio]
```

### Dominio (nucleo)
- Modelos (entidades, value objects), excepciones de dominio.
- Logica de negocio pura.
- NO importa nada de las otras capas.
- NO usa frameworks, ORMs, ni librerias externas.

### Aplicacion
- Casos de uso (un caso de uso = una accion del sistema).
- Define **puertos** (interfaces): entrada (driving) y salida (driven).
- Orquesta el dominio. NO contiene logica de negocio.
- Puede depender del dominio. NUNCA de infraestructura.

### Infraestructura
- **Adaptadores**: implementaciones concretas de los puertos.
- Controladores, repositorios, clientes HTTP, colas, etc.
- Depende de aplicacion y dominio. Es la capa mas externa.

## Reglas inquebrantables

1. **Regla de dependencia:** Las dependencias apuntan siempre hacia adentro (infra -> app -> dominio).
2. **Inversion de dependencias:** La aplicacion define puertos (interfaces). La infraestructura los implementa.
3. **Sin logica en adaptadores:** Un adaptador transforma datos y delega. No decide.
4. **Sin entidades anemicas:** Las entidades deben contener comportamiento, no solo datos.
5. **Un caso de uso, una clase/funcion:** No crear servicios genericos que agrupen multiples acciones.

## Anti-patrones a evitar

- Dominio que importa ORM o framework.
- Casos de uso que acceden directamente a la base de datos.
- Adaptadores con logica de negocio.
- Servicios "God class" que hacen de todo.
- Value Objects sin validacion.

## Estructura de carpetas simplificada

```
src/
  domain/
    models/
    exceptions/
  application/
    use_cases/
    ports/
  infrastructure/
    controllers/
    repositories/
    config/
tests/
  domain/
  application/
  infrastructure/
```

Esta estructura se adapta al lenguaje (ver docs del lenguaje correspondiente).
