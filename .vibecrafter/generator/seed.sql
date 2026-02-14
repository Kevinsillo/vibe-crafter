CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER REFERENCES steps(id),
    trigger_value TEXT,
    "order" INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('text', 'multiline', 'select', 'confirm')),
    question TEXT NOT NULL,
    options TEXT,
    variable TEXT NOT NULL,
    md_section TEXT,
    md_template TEXT,
    md_order INTEGER NOT NULL DEFAULT 0
);

-- Step 1: Nombre del proyecto
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (1, NULL, NULL, 1, 'text', 'Nombre del proyecto:', NULL, 'NOMBRE', 'datos_proyecto', '- **Nombre del proyecto:** {value}', 1);

-- Step 2: Descripcion breve
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (2, NULL, NULL, 2, 'text', 'Descripcion breve (1-2 frases):', NULL, 'DESC_BREVE', 'datos_proyecto', '- **Descripcion breve:** {value}', 2);

-- Step 3: Funcionalidades principales
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (3, NULL, NULL, 3, 'multiline', 'Lista las funcionalidades principales:', NULL, 'DESC_DETALLADA', 'datos_proyecto', '- **Descripcion detallada / funcionalidades:**\n{value}', 3);

-- Step 4: Lenguaje (escanea subdirectorios de docs/languages/)
-- Ahora va ANTES de tipo de proyecto para poder escanear project_types/ del lenguaje elegido
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (4, NULL, NULL, 4, 'select', 'Que lenguaje quieres usar?', '@scan:languages', 'LENGUAJE', 'datos_proyecto', '- **Lenguaje de programacion:** {value}\n  > Convenciones y testing: `.vibecrafter/docs/languages/{value}/`', 4);

-- Step 5: Tipo de proyecto (escanea project_types/ del lenguaje elegido)
-- {LENGUAJE} se resuelve en tiempo de ejecucion con el valor de la sesion
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (5, NULL, NULL, 5, 'select', 'Que tipo de proyecto es?', '@scan:languages/{LENGUAJE}/project_types', 'TIPO_PROYECTO', 'datos_proyecto', '- **Tipo de proyecto:** {value}\n  > Tipo de proyecto: `.vibecrafter/docs/languages/[lenguaje]/project_types/{value}.md`', 5);

-- Step 6: Frontend (hijo de step 5, trigger "webapp")
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (6, 5, 'webapp', 1, 'select', 'Como quieres el frontend?', 'Motor de plantillas HTML (server-side, mas simple)|Frontend separado (SPA con React, Vue, etc.)', 'WEBAPP_FRONTEND', 'datos_proyecto', '- **Frontend:** {value}', 6);

-- Step 7: Base de datos (escanea docs/databases/)
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (7, NULL, NULL, 6, 'select', 'Necesitas base de datos?', '@scan:databases|Ninguna', 'BASE_DATOS', 'contexto', '- **Base de datos:** {value}\n  > Base de datos: `.vibecrafter/docs/databases/{value}.md`\n  > Persistencia: `.vibecrafter/docs/languages/[lenguaje]/persistence.md`', 1);

-- Step 8: Autenticacion - Python (hijo de step 4, trigger "python")
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (8, 4, 'python', 1, 'select', 'Necesitas autenticacion?', 'No|JWT|OAuth2|Session', 'AUTH', 'contexto', '- **Autenticacion:** {value}\n  > Autenticacion: `.vibecrafter/docs/languages/[lenguaje]/auth.md`', 2);

-- Step 9: Testing
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (9, NULL, NULL, 7, 'select', 'Que tipo de testing quieres?', 'Unitarios|Integracion|Unitarios + Integracion|E2E|Ninguno', 'TESTING', 'contexto', '- **Testing:** {value}', 3);

-- Step 10: Diseno visual (hijo de step 5, trigger "webapp")
-- {value} = nombre del .md (ej: "material-ui"), se usa directamente en la ruta
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (10, 5, 'webapp', 2, 'select', 'Que estilo de diseno quieres aplicar?', '@scan:designs|Ninguno', 'DISENO', 'contexto', '- **Diseno visual:** {value}\n  > Estilos: `.vibecrafter/docs/designs/{value}.md`', 4);

-- Step 11: Diseno visual (hijo de step 5, trigger "cli")
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (11, 5, 'cli', 1, 'select', 'Que estilo de diseno quieres aplicar?', '@scan:designs|Ninguno', 'DISENO', 'contexto', '- **Diseno visual:** {value}\n  > Estilos: `.vibecrafter/docs/designs/{value}.md`', 4);

-- Step 12: Notas adicionales
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (12, NULL, NULL, 8, 'text', 'Notas adicionales (opcional, Enter para saltar):', NULL, 'NOTAS', 'contexto', '- **Notas extra:** {value}', 5);

-- Step 13: Autenticacion - Kotlin (hijo de step 4, trigger "kotlin")
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (13, 4, 'kotlin', 1, 'select', 'Necesitas autenticacion?', 'No|Firebase Auth|JWT (backend propio)|OAuth2', 'AUTH', 'contexto', '- **Autenticacion:** {value}\n  > Autenticacion: `.vibecrafter/docs/languages/[lenguaje]/auth.md`', 2);

-- Step 14: Diseno visual (hijo de step 5, trigger "android-app")
INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order)
VALUES (14, 5, 'android-app', 1, 'select', 'Que estilo de diseno quieres aplicar?', '@scan:designs|Ninguno', 'DISENO', 'contexto', '- **Diseno visual:** {value}\n  > Estilos: `.vibecrafter/docs/designs/{value}.md`', 4);
