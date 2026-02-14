# PostgreSQL - Convenciones de base de datos

## Cuando usarlo

- Aplicaciones con datos relacionales complejos.
- Proyectos que necesitan consultas avanzadas (JSON, full-text search, CTE).
- APIs y microservicios con alta concurrencia.
- Cuando se necesita integridad referencial fuerte.

## Estructura de esquema

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

- Usar `UUID` para claves primarias (evita IDs secuenciales predecibles).
- Usar `TIMESTAMPTZ` (con timezone), nunca `TIMESTAMP` sin zona.
- Usar `VARCHAR(n)` con limite explicito o `TEXT` si no hay limite logico.
- Crear indices para columnas de busqueda y foreign keys.

## Migraciones

### Herramientas recomendadas

- **Alembic** (Python): generacion automatica desde modelos SQLAlchemy.
- **Flyway** (JVM/generico): migraciones con ficheros SQL numerados.
- **golang-migrate** (Go): ligero, SQL puro.

### Estructura de migraciones

```
migrations/
  V001__create_users.sql
  V002__add_avatar_to_users.sql
  V003__create_orders.sql
```

### Tabla de versiones

Las herramientas de migracion crean una tabla automaticamente (ej: `alembic_version`, `flyway_schema_history`). No crearla manualmente.

### Convenciones de migraciones

```sql
-- V002__add_avatar_to_users.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- Siempre incluir rollback en un comentario o fichero separado:
-- ROLLBACK: ALTER TABLE users DROP COLUMN avatar_url;
```

- Cada migracion es un fichero SQL con un unico cambio logico.
- Nombres descriptivos: `V003__create_orders_table.sql`.
- Nunca modificar una migracion ya aplicada. Crear una nueva.
- Migraciones idempotentes cuando sea posible: `CREATE TABLE IF NOT EXISTS`.

## Connection pooling

- Usar siempre un pool de conexiones (no abrir/cerrar por cada query).
- Herramientas: `pgbouncer` (externo) o pool integrado en el ORM/driver.
- Tamano recomendado: `(num_cores * 2) + num_disks` como punto de partida.

## Esquemas (schemas)

```sql
CREATE SCHEMA IF NOT EXISTS app;
CREATE TABLE app.users ( ... );
```

- Usar esquemas para separar dominios dentro de la misma base.
- No acumular todo en `public`.

## Buenas practicas

- Transacciones para operaciones multiples: `BEGIN; ... COMMIT;`.
- `EXPLAIN ANALYZE` para diagnosticar queries lentas.
- Indices parciales para columnas con baja cardinalidad: `CREATE INDEX ... WHERE active = true`.
- Enums nativos para valores fijos: `CREATE TYPE status AS ENUM ('active', 'inactive')`.
- Constraints de base de datos como ultima barrera de validacion (la primera es el dominio).

## Anti-patrones

- Usar `SERIAL` en vez de `UUID` para IDs expuestos al exterior.
- Queries sin indice en tablas grandes.
- Almacenar JSON en columnas cuando los datos son relacionales y consultables.
- No usar transacciones en operaciones de escritura multiples.
- Conexiones sin pool en aplicaciones con concurrencia.
