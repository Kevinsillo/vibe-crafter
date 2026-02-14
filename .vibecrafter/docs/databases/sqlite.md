# SQLite - Convenciones de base de datos

## Cuando usarlo

- Almacenamiento local embebido (apps moviles, CLIs, apps de escritorio).
- Prototipado rapido sin servidor de base de datos.
- Proyectos que no requieren acceso concurrente de multiples procesos.

## Modo WAL (Write-Ahead Logging)

Activar siempre WAL para mejor rendimiento en lecturas concurrentes:

```sql
PRAGMA journal_mode=WAL;
```

- Permite lecturas simultaneas mientras se escribe.
- Mejora significativa en apps con muchas lecturas (patron tipico en mobile).

## Estructura de esquema

```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

CREATE INDEX idx_users_email ON users(email);
```

- Usar `TEXT` para UUIDs e IDs.
- Usar `INTEGER` para timestamps (Unix epoch), no `DATETIME`.
- Crear indices para columnas de busqueda frecuente.
- SQLite no tiene tipos estrictos por defecto. Usar `STRICT` tables si la version lo soporta (3.37+).

## Migraciones

### Tabla de versiones

SQLite no tiene sistema de migraciones nativo. Usar `PRAGMA user_version` para rastrear la version del esquema:

```sql
PRAGMA user_version = 1;  -- Establecer version
PRAGMA user_version;       -- Consultar version actual
```

### Estrategia de migraciones

Crear ficheros SQL numerados secuencialmente:

```
migrations/
  001_create_users.sql
  002_add_avatar_to_users.sql
  003_create_orders.sql
```

Cada fichero contiene los cambios de esa version:

```sql
-- 002_add_avatar_to_users.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;
PRAGMA user_version = 2;
```

### Limitaciones de ALTER TABLE

SQLite tiene `ALTER TABLE` limitado. No soporta:
- `DROP COLUMN` (si, desde 3.35.0).
- `RENAME COLUMN` (si, desde 3.25.0).
- Cambiar tipo de columna o constraints.

Para cambios complejos, usar la estrategia de recreacion:

```sql
-- 1. Crear tabla nueva con el esquema deseado
CREATE TABLE users_new (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- 2. Copiar datos
INSERT INTO users_new SELECT id, name, email FROM users;

-- 3. Eliminar tabla vieja
DROP TABLE users;

-- 4. Renombrar
ALTER TABLE users_new RENAME TO users;
```

## Buenas practicas

- Activar foreign keys explicitamente: `PRAGMA foreign_keys = ON;` (desactivadas por defecto).
- Usar transacciones para operaciones multiples: `BEGIN; ... COMMIT;`.
- No almacenar blobs grandes (imagenes, archivos). Guardar la ruta al fichero.
- Fichero `.db` en directorio con permisos adecuados (no accesible publicamente).
- Backups con `.backup` o copiando el fichero con la base cerrada.

## Anti-patrones

- Usar `AUTOINCREMENT` sin necesidad (es mas lento que `INTEGER PRIMARY KEY` solo).
- Asumir que foreign keys estan activas sin el `PRAGMA`.
- Almacenar JSON como texto sin necesidad (usar tablas normalizadas).
- Multiples procesos escribiendo al mismo fichero sin WAL.
