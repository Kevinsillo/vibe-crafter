# INSTRUCCIONES PARA EL AGENTE (NO MODIFICAR)

> Lo que sigue es el punto de entrada del sistema de instrucciones.
> El agente DEBE seguir estas fases en orden. No puede saltarse ninguna.

---

## Fase 0 - Lectura y comprension del formulario

1. Lee todo el formulario de arriba.
2. Identifica: nombre, tipo de proyecto, lenguaje, funcionalidades y contexto adicional.
3. Si algo esta ambiguo o incompleto, pregunta al usuario ANTES de continuar.

---

## Fase 1 - Carga de conocimiento obligatorio (Nivel 1)

Lee los siguientes documentos en este orden:

1. `.vibecrafter/common/hexagonal.md`
2. `.vibecrafter/common/good-practices.md`
3. `.vibecrafter/common/testing.md`

Despues de leerlos, DEBES declarar:

- Las reglas arquitectonicas que vas a respetar.
- Las dependencias permitidas entre capas.
- Lo que NO vas a hacer (anti-patrones a evitar).

Si no puedes verbalizarlo, NO avances a la siguiente fase.

---

## Fase 2 - Carga de conocimiento por lenguaje (Nivel 1)

Segun el lenguaje indicado en el formulario, lee los documentos base de la carpeta correspondiente:

| Lenguaje   | Ruta                                   |
|------------|----------------------------------------|
| Python     | `.vibecrafter/languages/python/`       |
| TypeScript | `.vibecrafter/languages/typescript/`   |
| Java       | `.vibecrafter/languages/java/`         |
| Go         | `.vibecrafter/languages/go/`           |

Lee los documentos base: `conventions.md` y `testing.md`.

---

## Fase 3 - Carga condicional (Nivel 2)

Lee estos documentos adicionales segun lo indicado en el formulario. Sustituye `[lang]` por el lenguaje en minusculas (python, typescript, java, go):

| Condicion                        | Documento                                          |
|----------------------------------|-----------------------------------------------------|
| Siempre (tipo de proyecto)       | `.vibecrafter/languages/[lang]/project_types/[tipo].md` |
| Usa base de datos (!= Ninguna)   | `.vibecrafter/languages/[lang]/persistence.md`      |
| Usa autenticacion (!= No)        | `.vibecrafter/languages/[lang]/auth.md`             |
| Usa mensajeria/eventos           | `.vibecrafter/languages/[lang]/messaging.md`        |
| Tiene diseno visual              | `.vibecrafter/designs/[diseno].md`                  |

Mapeo de tipo de proyecto a fichero:
- API REST → `api-rest.md`
- CLI → `cli.md`
- Web app → `webapp.md`
- Microservicio → `microservice.md`
- Libreria → `library.md`

Para cada documento, justifica por que es necesario.

---

## Fase 4 - Diseno conceptual

ANTES de escribir codigo, genera y presenta al usuario:

1. **Limites del dominio:** Que entidades y value objects existen.
2. **Casos de uso:** Lista explicita. Cada caso de uso debe tener nombre, entrada, salida y reglas.
3. **Decisiones descartadas:** Que decidiste NO hacer y por que.
4. **Estructura de modulos:** Arbol de carpetas propuesto.

Regla: No se puede crear un adaptador si no existe al menos un caso de uso que lo consuma.

Espera aprobacion del usuario antes de continuar.

---

## Fase 5 - Creacion de estructura

ANTES de escribir logica, crea:

1. Toda la estructura de carpetas del proyecto.
2. Todos los ficheros vacios necesarios.
3. El fichero de configuracion del proyecto (`pyproject.toml`, `package.json`, etc.) sin dependencias.
4. El Makefile u equivalente con los comandos basicos.

Esto permite al usuario ver la estructura completa antes de generar codigo.

---

## Fase 6 - Generacion de codigo

Genera el codigo siguiendo:

- La arquitectura validada en Fase 4.
- Las convenciones del lenguaje (Fase 2).
- Las reglas de hexagonal y buenas practicas (Fase 1).
- El diseno visual si aplica (Fase 3).
- Las web apps son **mobile first y responsive** por defecto.

Orden de generacion:
1. Dominio (modelos, excepciones de dominio)
2. Aplicacion (casos de uso, puertos)
3. Infraestructura (controladores, repositorios, configuracion)
4. Tests (segun reglas de `.vibecrafter/common/testing.md`)

Regla: cada caso de uso debe tener al menos un test antes de pasar al siguiente.

Las dependencias se agregan por consola (ej: `poetry add`, `npm install`), no se escriben manualmente en el fichero de configuracion.

---

## Fase 7 - Revision

Al terminar, realiza una autoevaluacion:

- [ ] El dominio NO importa nada de infraestructura.
- [ ] Cada caso de uso tiene al menos un test.
- [ ] Los adaptadores implementan puertos, no logica de negocio.
- [ ] No hay servicios genericos inflados (God Services).
- [ ] La estructura de carpetas coincide con el diseno aprobado.
- [ ] Se ha generado un README tecnico minimo.

Lista las reglas violadas (si las hay) y la deuda tecnica consciente.
