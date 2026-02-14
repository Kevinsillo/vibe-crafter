# Firebase Firestore - Convenciones de base de datos

## Cuando usarlo

- Aplicaciones moviles que necesitan sincronizacion en tiempo real.
- Proyectos con soporte offline nativo.
- Cuando se quiere evitar gestionar un servidor de base de datos.
- Apps con modelo de datos basado en documentos y colecciones.

## Modelado de datos

### Estructura: colecciones y documentos

```
users/                          (coleccion)
  user-123/                     (documento)
    name: "Ana"
    email: "ana@mail.com"
    created_at: Timestamp
    orders/                     (subcoleccion)
      order-456/                (documento)
        items: [...]
        total: 19.98
```

### Documento plano (preferido)

```json
{
  "name": "Ana",
  "email": "ana@mail.com",
  "address": {
    "street": "Calle Mayor 1",
    "city": "Madrid"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Subcolecciones vs campos anidados

- **Campos anidados** (maps): datos que siempre se leen con el documento padre. Ej: direccion de un usuario.
- **Subcolecciones**: datos que crecen independientemente o se consultan por separado. Ej: mensajes de un chat.

### Regla para decidir

- **Anidar** si los datos son pocos, fijos y se leen siempre juntos.
- **Subcoleccion** si los datos crecen, se paginan o se consultan independientemente.

## Indices

### Indices automaticos

Firestore crea un indice automatico por cada campo individual. No es necesario crearlos manualmente para consultas sobre un solo campo.

### Indices compuestos

Necesarios para queries con multiples campos o combinaciones de filtro + ordenacion:

```
// Indice compuesto (definir en firestore.indexes.json)
{
  "collectionGroup": "orders",
  "fields": [
    { "fieldPath": "user_id", "order": "ASCENDING" },
    { "fieldPath": "created_at", "order": "DESCENDING" }
  ]
}
```

Firestore sugiere indices compuestos automaticamente cuando una query los necesita (muestra un link en el error).

## Versionado de esquema

Firestore no tiene esquema formal. Los documentos pueden tener campos diferentes. Estrategias para evolucionar:

### Campo de version

```json
{
  "schema_version": 2,
  "name": "Ana",
  "email": "ana@mail.com",
  "avatar_url": null
}
```

### Migraciones con Cloud Functions o scripts

```
migrations/
  001_add_avatar_to_users.ts
  002_normalize_emails.ts
```

```typescript
// 001_add_avatar_to_users.ts
const snapshot = await db.collection('users')
  .where('schema_version', '<', 2)
  .get();

const batch = db.batch();
snapshot.docs.forEach(doc => {
  batch.update(doc.ref, {
    avatar_url: null,
    schema_version: 2
  });
});
await batch.commit();
```

- Usar batch writes (maximo 500 operaciones por batch).
- Ejecutar migraciones como scripts one-off o Cloud Functions.

## Security Rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
    }

    match /users/{userId}/orders/{orderId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

- **Nunca** dejar reglas abiertas (`allow read, write: if true`) en produccion.
- Validar estructura del documento en las reglas.
- Testear reglas con el emulador local de Firebase.

## Soporte offline

Firestore tiene cache offline activada por defecto en mobile. Los datos se sincronizan automaticamente al recuperar conexion.

```kotlin
// Android: configurar persistencia (activada por defecto)
val settings = firestoreSettings {
    isPersistenceEnabled = true
    cacheSizeBytes = FirebaseFirestoreSettings.CACHE_SIZE_UNLIMITED
}
firestore.firestoreSettings = settings
```

## Buenas practicas

- Nombrar colecciones en plural y snake_case: `users`, `chat_messages`.
- IDs de documento: usar IDs con significado si existe (ej: `userId`), auto-generado si no.
- Desnormalizar datos que se leen juntos frecuentemente.
- Limitar el tamano de documentos (maximo 1 MB por documento).
- Paginar queries grandes con `startAfter()` / `limit()`.
- Usar el emulador local para desarrollo y testing.

## Anti-patrones

- Documentos que crecen sin limite (arrays con miles de elementos).
- Queries profundas con multiples `where` sin indice compuesto.
- Leer colecciones enteras cuando solo se necesitan unos documentos.
- Security rules abiertas o inexistentes.
- Usar Firestore como base de datos relacional (joins manuales excesivos).
- Guardar datos que cambian muy frecuentemente en el mismo documento (ej: contadores de alta frecuencia, usar `increment()` o Realtime Database).
