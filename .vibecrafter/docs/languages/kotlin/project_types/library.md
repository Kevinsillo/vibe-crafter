# Kotlin - Libreria (Nivel 2)

> Solo leer si el tipo de proyecto es Libreria Android/Kotlin.

## Herramientas recomendadas

- **Gradle KTS** con plugin `com.android.library` o `kotlin("jvm")` segun el caso.
- **JUnit 5** + **MockK** para testing.
- **Dokka** para documentacion (KDoc -> HTML/Javadoc).
- **Maven Publish** plugin para publicacion.
- **API Validator** (`binary-compatibility-validator`) para controlar cambios en la API publica.

## Tipos de libreria

### Android Library (`com.android.library`)
Para librerias que dependen del SDK de Android (UI, Context, recursos).

### Kotlin/JVM Library (`kotlin("jvm")`)
Para librerias puras de Kotlin sin dependencias de Android. Reutilizables en backend, CLI o multiplataforma.

## Estructura

```
mi-libreria/
  build.gradle.kts
  src/
    main/
      kotlin/com/ejemplo/milibreria/
        core/              # logica principal (dominio)
          models/
          exceptions/
        services/          # operaciones publicas (aplicacion)
        adapters/          # implementaciones opcionales (infraestructura)
      AndroidManifest.xml  # solo si es Android Library
    test/
      kotlin/com/ejemplo/milibreria/
        core/
        services/
```

## API publica

Controlar la superficie publica con `internal`:

```kotlin
// Publico: el usuario de la libreria puede usarlo
class ImageProcessor(
    private val config: ProcessorConfig,
) {
    fun process(input: ByteArray): ProcessedImage { ... }
}

data class ProcessorConfig(
    val quality: Int = 80,
    val maxWidth: Int = 1920,
)

// Interno: solo visible dentro del modulo
internal class ImageDecoder {
    fun decode(bytes: ByteArray): RawImage { ... }
}
```

Todo lo que no deba ser publico debe ser `internal` o `private`. Kotlin ofrece `internal` a nivel de modulo, usarlo siempre.

## build.gradle.kts para Android Library

```kotlin
plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    id("maven-publish")
}

android {
    namespace = "com.ejemplo.milibreria"
    compileSdk = 35

    defaultConfig {
        minSdk = 26
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

publishing {
    publications {
        create<MavenPublication>("release") {
            groupId = "com.ejemplo"
            artifactId = "mi-libreria"
            version = "1.0.0"
            afterEvaluate {
                from(components["release"])
            }
        }
    }
}
```

## build.gradle.kts para Kotlin/JVM Library

```kotlin
plugins {
    kotlin("jvm")
    id("maven-publish")
}

kotlin {
    jvmToolchain(17)
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            groupId = "com.ejemplo"
            artifactId = "mi-libreria"
            version = "1.0.0"
            from(components["java"])
        }
    }
}
```

## Documentacion con KDoc

```kotlin
/**
 * Procesa una imagen aplicando compresion y redimensionado.
 *
 * @param input bytes de la imagen original
 * @return imagen procesada con los parametros de configuracion
 * @throws InvalidImageException si el formato no es soportado
 */
fun process(input: ByteArray): ProcessedImage { ... }
```

Generar documentacion con Dokka:

```kotlin
plugins {
    id("org.jetbrains.dokka") version "1.9.20"
}
```

## Reglas

- API publica minima: todo lo que no sea API es `internal`.
- Evitar dependencias pesadas. Cada dependencia transitiva es un coste para el consumidor.
- Type hints completos en la API publica (no usar `Any` ni tipos genericos sin restriccion).
- KDoc en clases y funciones publicas.
- Versionado semantico (semver).
- Tests con cobertura alta del core (>80%).
- No exponer detalles de implementacion (clases internas, DTOs, excepciones de librerias de terceros).
- Si la libreria usa coroutines, documentar el dispatcher esperado o usar `withContext` internamente.

## Anti-patrones a evitar

- Exponer clases de terceros en la API publica (ej: tipos de Retrofit, Room).
- Dependencias con version fija que conflicten con el proyecto consumidor.
- Inicializacion implicita con `ContentProvider` (preferir inicializacion explicita).
- Forzar un framework de DI especifico al consumidor.
