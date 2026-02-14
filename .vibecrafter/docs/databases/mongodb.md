# MongoDB - Convenciones de base de datos

## Cuando usarlo

- Datos con esquema flexible o que cambian frecuentemente.
- Documentos con estructura anidada natural (ej: pedido con lineas de pedido).
- Proyectos que necesitan escalabilidad horizontal.
- Cuando el patron de acceso es por documento completo, no por joins.

## Modelado de datos

### Documento embebido (preferido cuando se accede junto)

```json
{
  "_id": "user-123",
  "name": "Ana",
  "email": "ana@mail.com",
  "addresses": [
    {
      "street": "Calle Mayor 1",
      "city": "Madrid",
      "zip": "28001"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Referencia (cuando el subdocumento crece independientemente)

```json
// Coleccion: users
{
  "_id": "user-123",
  "name": "Ana",
  "email": "ana@mail.com"
}

// Coleccion: orders
{
  "_id": "order-456",
  "user_id": "user-123",
  "items": [
    { "product": "Widget", "quantity": 2, "price": 9.99 }
  ],
  "total": 19.98
}
```

### Regla para decidir

- **Embeber** si los datos se leen juntos y el subdocumento no crece sin limite.
- **Referenciar** si los datos se acceden independientemente o el subdocumento puede crecer indefinidamente.

## Indices

```javascript
db.users.createIndex({ email: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1 });
db.orders.createIndex({ created_at: -1 });
```

- Crear indices para todos los campos de consulta.
- Indices compuestos: poner la columna mas selectiva primero.
- Usar `explain()` para verificar que las queries usan indices.

## Migraciones / versionado de esquema

MongoDB no tiene esquema formal, pero los documentos evolucionan. Estrategias:

### Campo de version en el documento

```json
{
  "_id": "user-123",
  "schema_version": 2,
  "name": "Ana",
  "email": "ana@mail.com",
  "avatar_url": null
}
```

### Scripts de migracion

```
migrations/
  001_add_avatar_to_users.js
  002_normalize_emails.js
```

```javascript
// 001_add_avatar_to_users.js
db.users.updateMany(
  { avatar_url: { $exists: false } },
  { $set: { avatar_url: null, schema_version: 2 } }
);
```

### Migracion lazy (on-read)

Transformar el documento al leerlo si tiene version antigua. Guardar la version nueva al escribir. Util cuando la migracion masiva es costosa.

## Coleccion de registro de migraciones

```javascript
db.migrations.insertOne({
  version: 1,
  name: "add_avatar_to_users",
  applied_at: new Date()
});
```

Consultar antes de ejecutar para evitar doble aplicacion.

## Validacion de esquema

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email"],
      properties: {
        name: { bsonType: "string" },
        email: { bsonType: "string" }
      }
    }
  }
});
```

Usar `$jsonSchema` para validar estructura minima a nivel de base de datos.

## Buenas practicas

- Nombrar colecciones en plural y snake_case: `users`, `order_items`.
- Usar `_id` personalizado si tiene significado de negocio. Si no, dejar que MongoDB genere `ObjectId`.
- No abusar del embedding: documentos mayores a 16 MB fallan.
- Indices para todas las queries frecuentes.
- Transacciones multi-documento solo cuando sea estrictamente necesario (a partir de MongoDB 4.0).

## Anti-patrones

- Modelar MongoDB como si fuera SQL (normalizar todo con referencias).
- Documentos que crecen sin limite (arrays que se expanden indefinidamente).
- Queries sin indice en colecciones grandes.
- Ignorar el tamaño del working set (debe caber en RAM).
- Usar `$lookup` (join) como patron principal de acceso.
