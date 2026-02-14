# MySQL - Convenciones de base de datos

## Cuando usarlo

- Aplicaciones web con datos relacionales.
- Proyectos que necesitan replicacion y alta disponibilidad.
- Cuando el equipo ya tiene experiencia con MySQL/MariaDB.

## Estructura de esquema

```sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_users_email ON users(email);
```

- Usar `InnoDB` siempre (soporte de transacciones y foreign keys).
- Usar `utf8mb4` como charset (soporta emojis y caracteres unicode completos). `utf8` de MySQL solo soporta 3 bytes.
- Usar `CHAR(36)` para UUIDs o `BINARY(16)` para almacenamiento compacto.
- `ON UPDATE CURRENT_TIMESTAMP` para `updated_at` automatico.

## Migraciones

### Herramientas recomendadas

- **Alembic** (Python): generacion automatica desde modelos SQLAlchemy.
- **Flyway** (JVM/generico): migraciones con ficheros SQL numerados.
- **Liquibase** (JVM): migraciones en XML, YAML, SQL o JSON.

### Estructura de migraciones

```
migrations/
  V001__create_users.sql
  V002__add_avatar_to_users.sql
  V003__create_orders.sql
```

### Convenciones

```sql
-- V002__add_avatar_to_users.sql
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500) NULL;
```

- Cada fichero contiene un unico cambio logico.
- Nunca modificar migraciones aplicadas.
- Incluir rollback como comentario o fichero separado.

## Tipos de datos recomendados

| Dato | Tipo MySQL | Notas |
|------|-----------|-------|
| ID (UUID) | `CHAR(36)` o `BINARY(16)` | `CHAR` mas legible, `BINARY` mas eficiente |
| Texto corto | `VARCHAR(n)` | Siempre con limite explicito |
| Texto largo | `TEXT` | No indexable directamente |
| Fecha/hora | `TIMESTAMP` | Almacena en UTC internamente |
| Dinero | `DECIMAL(10,2)` | Nunca `FLOAT` ni `DOUBLE` |
| Booleano | `TINYINT(1)` | MySQL no tiene tipo `BOOLEAN` real |
| Enum | `ENUM('a','b')` | Util para valores fijos, dificil de migrar |

## Modos SQL

Activar modo estricto para evitar truncamientos silenciosos:

```sql
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

## Buenas practicas

- `EXPLAIN` para diagnosticar queries lentas.
- Indices compuestos: columna mas selectiva primero.
- Connection pooling obligatorio en aplicaciones con concurrencia.
- Usar transacciones: `START TRANSACTION; ... COMMIT;`.
- Backups con `mysqldump --single-transaction` para InnoDB.

## Anti-patrones

- Usar `utf8` en vez de `utf8mb4`.
- Usar `MyISAM` (sin transacciones, sin foreign keys).
- `SELECT *` en tablas con muchas columnas.
- No usar modo estricto (MySQL trunca datos silenciosamente por defecto).
- Almacenar fechas como strings.
