# Oracle Java Bot — Guía de usuario

> **Versión:** Sprint 3 · Module 2 · May 2026
> **Aplica a:** Oracle Java Bot v1.0 (Sprint 3 release)
> **Tech stack:** React 18 / TypeScript · Spring Boot 3 / Java 21 · Python 3 AI Service · Oracle Autonomous Database (ATP)
> **Navegadores compatibles:** Chrome 124+, Firefox 125+, Edge 124+
> **Última validación:** May 2026 — Sprint 3 acceptance testing

---

## Tabla de contenido

- [Inicio rápido — En funcionamiento en 5 minutos](#inicio-rápido--en-funcionamiento-en-5-minutos)
- [Descripción general del sistema](#descripción-general-del-sistema)
- [Glosario](#glosario)
- [Prerrequisitos y acceso](#prerrequisitos-y-acceso)
- [Cómo iniciar sesión](#cómo-iniciar-sesión)
- **Inicio — Tu Portfolio Dashboard**
  - [Cómo leer tu Portfolio Overview](#cómo-leer-tu-portfolio-overview)
  - [Cómo interpretar las KPI Cards](#cómo-interpretar-las-kpi-cards)
  - [Cómo leer los Portfolio Charts](#cómo-leer-los-portfolio-charts)
  - [Cómo navegar a un Proyecto desde el Dashboard](#cómo-navegar-a-un-proyecto-desde-el-dashboard)
- **Tareas — Task Management**
  - [Cómo filtrar Tareas por Proyecto y Sprint](#cómo-filtrar-tareas-por-proyecto-y-sprint)
  - [Cómo crear una nueva Tarea](#cómo-crear-una-nueva-tarea)
  - [Cómo ver y editar los detalles de una Tarea](#cómo-ver-y-editar-los-detalles-de-una-tarea)
  - [Cómo actualizar el Estado de una Tarea](#cómo-actualizar-el-estado-de-una-tarea)
  - [Cómo eliminar una Tarea](#cómo-eliminar-una-tarea)
- **Agent — AI-Powered Automation**
  - [Cómo generar Tareas automáticamente con AI](#cómo-generar-tareas-automáticamente-con-ai)
  - [Cómo revisar, editar y aprobar sugerencias de Tareas de AI](#cómo-revisar-editar-y-aprobar-sugerencias-de-tareas-de-ai)
  - [Cómo ejecutar un análisis de Tareas duplicadas](#cómo-ejecutar-un-análisis-de-tareas-duplicadas)
  - [Cómo revisar y eliminar Tareas duplicadas](#cómo-revisar-y-eliminar-tareas-duplicadas)
- **Proyectos — Project Management**
  - [Cómo explorar y filtrar Proyectos](#cómo-explorar-y-filtrar-proyectos)
  - [Cómo crear un nuevo Proyecto](#cómo-crear-un-nuevo-proyecto)
  - [Cómo ver el KPI Dashboard de un Proyecto](#cómo-ver-el-kpi-dashboard-de-un-proyecto)
  - [Cómo editar o eliminar un Proyecto](#cómo-editar-o-eliminar-un-proyecto)
- **Equipo — Team Management**
  - [Cómo explorar tus Equipos](#cómo-explorar-tus-equipos)
  - [Cómo crear un nuevo Equipo](#cómo-crear-un-nuevo-equipo)
  - [Cómo agregar o quitar un miembro de Equipo](#cómo-agregar-o-quitar-un-miembro-de-equipo)
  - [Cómo editar la Description de un Equipo](#cómo-editar-la-description-de-un-equipo)
- **Telegram Bot — Developer Interface**
  - [Cómo conectar tu cuenta de Telegram](#cómo-conectar-tu-cuenta-de-telegram)
  - [Cómo seleccionar tu Proyecto activo](#cómo-seleccionar-tu-proyecto-activo)
  - [Cómo ver y actualizar tus Tareas](#cómo-ver-y-actualizar-tus-tareas)
  - [Cómo agregar una Tarea mediante Telegram](#cómo-agregar-una-tarea-mediante-telegram)
  - [Referencia de comandos del Bot](#referencia-de-comandos-del-bot)
- [Solución de problemas y errores comunes](#solución-de-problemas-y-errores-comunes)
- [Información de versión y entorno](#información-de-versión-y-entorno)
- [Feedback](#feedback)

---

## Inicio rápido — En funcionamiento en 5 minutos

### Como Manager

1. Inicia sesión en el web dashboard.
2. Ve a **Equipo** → haz clic en **+ Nuevo equipo** → ingresa un nombre y owner → haz clic en **Guardar**.
3. Ve a **Proyectos** → haz clic en **+ Nuevo proyecto** → completa un nombre y fechas → haz clic en **Crear proyecto**.
4. Ve a **Tareas** → haz clic en **+ Nueva tarea** → completa el título, proyecto, prioridad y fecha límite → haz clic en **Guardar**.
5. En la página **Inicio** ya verás tu nuevo proyecto en la tabla "Proyectos en curso" con una barra de progreso en vivo.

### Como Developer

1. Pídele a tu Manager el nombre del Telegram bot y confirma que hayan registrado tu Telegram ID.
2. Abre Telegram, busca el bot y toca **Start** (o escribe `/start` y presiona [Send]).
3. Toca **Select Project** y elige tu proyecto.
4. Toca **List All Tasks** para ver tus tareas asignadas.
5. Toca **IN PROGRESS** en la tarea en la que estás trabajando — el estado se actualiza en el web dashboard en tiempo real.

> **Pro Tip:** Managers — ejecuten el flujo **Agent → Generar tareas** para permitir que AI prepare un borrador del backlog del sprint antes de que empiece el sprint; luego revisen y aprueben las sugerencias en un solo paso.

---

## Descripción general del sistema

Oracle Java Bot es una plataforma de project management para equipos de software. El web dashboard (para Managers) y el Telegram bot (para Developers) se mantienen sincronizados en tiempo real mediante una backend API compartida y un AI service.

| Componente | Quién lo usa | Propósito |
|---|---|---|
| **Web Dashboard** | Managers | Las 5 páginas: Inicio, Tareas, Agent, Proyectos, Equipo |
| **Telegram Bot** | Developers | Visibilidad de tareas y actualizaciones de estado en móvil |
| **Backend API** | System | REST API — almacena todos los datos y conecta web y bot |
| **AI Service** | System | Genera sugerencias de tareas y detecta duplicados |

### Resumen de roles

| Rol | Qué puede hacer |
|---|---|
| **Manager** | Acceso completo a todas las páginas; crear/editar/eliminar proyectos, equipos y tareas; acceder a funciones de AI |
| **Developer** | Acceso web de solo lectura; gestión completa de tareas mediante el Telegram bot |

---

## Glosario

| Término | Definición |
|---|---|
| **Equipo** | Un grupo de equipo que posee uno o más proyectos y contiene una lista de usuarios. |
| **Proyecto** | Un proyecto vinculado a un equipo. Contiene sprints y tareas. |
| **Sprint** | Un periodo de trabajo delimitado por tiempo dentro de un proyecto. Las tareas se asignan a un sprint. |
| **Tarea** | Una tarea individual con título, descripción, prioridad, fecha límite, horas estimadas, estado y persona(s) asignada(s). |
| **Estado** | Estado de tarea: **Por hacer** (To Do), **En progreso** (In Progress), **Completada** (Done) o **Cancelada** (Cancelled). |
| **Prioridad** | Urgencia de la tarea: **Alta** (High), **Media** (Medium), **Baja** (Low). |
| **KPI** | Una métrica Key Performance Indicator calculada por sprint o en todo el portafolio. |
| **Estimation Precision** | Relación entre horas estimadas y horas reales registradas. 1.0 = perfecto. Rango aceptable: 0.9 – 1.1. |
| **Telegram ID** | El username único de Telegram o ID numérico usado para vincular un usuario con el bot. |
| **Pipeline** | La secuencia de procesamiento de AI de múltiples pasos que se ejecuta durante el análisis de duplicados. |
| **Threshold** | El punto de corte de puntuación de similitud usado durante la detección de duplicados (predeterminado: 0.88). |
| **Embedding** | Una representación vectorial numérica del texto de una tarea, usada para comparación semántica por los motores de AI. |

---

## Prerrequisitos y acceso

### Qué necesitas antes de empezar

| Rol | Requisitos |
|---|---|
| **Manager** | Credenciales de inicio de sesión (email + password) para el web dashboard |
| **Developer** | Una cuenta de Telegram; tu Telegram ID registrado por un Manager en el web dashboard |

### Requisitos del sistema

- **Web dashboard** — Chrome 124+, Firefox 125+ o Edge 124+. No se requiere instalación.
- **Telegram bot** — app de Telegram en Android, iOS o desktop.
- **Network** — conexión estable a internet.

> **Caution:** Los Developers no pueden usar el Telegram bot hasta que un Manager haya registrado su **Telegram ID** en el web dashboard. El Manager debe completar este paso antes de que el developer intente usar `/start`.

---

## Cómo iniciar sesión

1. Abre la URL del dashboard de Oracle Java Bot en tu navegador.
2. Ingresa tu **Email** y **Password**.
3. Haz clic en **Iniciar sesión**.
4. Serás redirigido a la página **Inicio**.

> **Pro Tip:** Tu sesión persiste durante la sesión del navegador. Cerrar la pestaña o ventana requerirá que vuelvas a iniciar sesión.

---

## Inicio — Tu Portfolio Dashboard

La página **Inicio** (`/`) es la primera pantalla después de iniciar sesión. Le da a Managers una vista de portafolio en vivo y entre proyectos.

### Cómo leer tu Portfolio Overview

La parte superior de la página muestra la tabla **"Proyectos en curso"**, que lista todos los proyectos activos con:

- **Proyecto** — nombre del proyecto (clicable — abre el KPI dashboard del proyecto)
- **Progreso** — una barra de progreso que muestra el porcentaje general de completitud
- **Inicio** — fecha de inicio del proyecto
- **Fin** — fecha de fin del proyecto

Debajo de la tabla, cuatro stat cards resumen todo el portafolio de un vistazo:

| Card | Qué muestra |
|---|---|
| ⚡ **Proyectos activos** | Proyectos con progreso menor a 100% |
| ⬡ **Equipos** | Número total de equipos |
| ◈ **Proyectos** | Número total de proyectos en todos los equipos |
| ✓ **Completados (100%)** | Proyectos que han alcanzado 100% de progreso |

---

### Cómo interpretar las KPI Cards

El **Manager Portfolio Dashboard** (lado derecho de la página) muestra cinco KPI cards agregadas en los proyectos seleccionados:

| KPI Card | Qué mide |
|---|---|
| **Avg General Progress** | Porcentaje promedio de completitud en los proyectos seleccionados |
| **Avg Sprint Completion** | Porcentaje promedio de tareas planificadas del sprint que fueron completadas |
| **Avg On-Time Delivery** | Porcentaje promedio de tareas completadas que terminaron en su fecha límite o antes |
| **Avg Estimation Precision** | Relación promedio entre horas estimadas y horas reales (mientras más cerca de 1.0, mejor) |
| **Total Active Tasks** | Suma de todas las tareas en sprints activos de los proyectos seleccionados |

Para cambiar qué proyectos aparecen en las KPI cards y charts:

1. Haz clic en el dropdown multi-select **Projects**.
2. Marca o desmarca proyectos individuales, o usa **Select all** / **Unselect all**.
3. Las KPI cards y los tres charts se actualizan inmediatamente.

---

### Cómo leer los Portfolio Charts

Debajo de las KPI cards aparecen tres charts:

**Delivery Health** (stacked bar)
- Cada barra representa un proyecto.
- La porción verde = tareas completadas a tiempo.
- La porción roja = tareas completadas tarde.
- Úsalo para identificar qué proyectos tienen una alta proporción de entregas retrasadas.

**Estimation vs Real (hrs)** (grouped bar)
- Cada proyecto tiene dos barras: estimated hours (azul) y real hours (ámbar).
- Una barra real más alta que la estimada indica que el equipo subestimó el trabajo.
- Una barra real más baja indica que las tareas se completaron más rápido de lo planeado.

**Resource Workload / Productivity** (horizontal bar)
- Una barra por developer, que muestra el total de tareas completadas en los proyectos seleccionados.
- Úsalo para identificar desequilibrios de workload en el equipo.

---

### Cómo navegar a un Proyecto desde el Dashboard

1. En la tabla **"Proyectos en curso"**, haz clic en la fila del proyecto que quieras.
2. Irás directamente al KPI dashboard de ese proyecto (`/proyectos/:projectId`).

---

## Tareas — Task Management

La página **Tareas** (`/tareas`) muestra todas las tareas de tus proyectos organizadas en un tablero Kanban por estado.

### Cómo filtrar Tareas por Proyecto y Sprint

1. Navega a **Tareas** desde la barra de navegación.
2. En el dropdown **Proyectos**, selecciona uno o más proyectos. Usa **Sel. todo** para seleccionar todos a la vez.
3. En el dropdown **Filtrar por Sprints**, selecciona uno o más sprints.
4. El badge de conteo de tareas se actualiza para mostrar cuántas tareas coinciden con los filtros actuales.
5. El tablero Kanban se actualiza para mostrar solo las tareas filtradas.

> **Pro Tip:** Tu selección de proyecto se recuerda en el navegador entre sesiones — no tendrás que volver a seleccionar los mismos proyectos cada vez que abras la página.

---

### Cómo crear una nueva Tarea

1. Asegúrate de que al menos un proyecto esté seleccionado en el filtro de proyectos.
2. Haz clic en **+ Nueva tarea** en la esquina superior derecha.
3. Completa el formulario:
   - **Título** — nombre de la tarea (requerido)
   - **Descripción** — detalle opcional
   - **Proyecto** — selecciona el proyecto al que pertenece esta tarea (requerido)
   - **Sprint** — asigna a un sprint
   - **Fecha límite** — fecha límite
   - **Prioridad** — Alta, Media o Baja
   - **Tiempo estimado** — horas estimadas (opcional)
4. Haz clic en **Guardar**.
5. La tarea aparece en la columna **Por hacer** del tablero Kanban.

> **Caution:** El botón **+ Nueva tarea** está deshabilitado si no hay ningún proyecto seleccionado en el filtro. Selecciona al menos un proyecto primero.

---

### Cómo ver y editar los detalles de una Tarea

1. Haz clic en cualquier task card del tablero Kanban.
2. Se abre un side panel a la derecha que muestra los detalles completos de la tarea, incluyendo descripción, persona(s) asignada(s), historial de estado y seguimiento de tiempo.
3. Edita los campos directamente en el side panel.
4. Cierra el panel haciendo clic en el botón **✕** o haciendo clic fuera del panel.

---

### Cómo actualizar el Estado de una Tarea

Desde el tablero Kanban, arrastra una task card y suéltala en la columna de estado objetivo:

- **Por hacer** → la tarea no ha sido iniciada
- **En progreso** → la tarea se está trabajando activamente
- **Completada** → la tarea está terminada
- **Cancelada** → la tarea no se completará

Como alternativa, abre el side panel de la tarea y cambia el estado ahí.

> **Pro Tip:** Los cambios de estado realizados aquí se reflejan en el Telegram bot en tiempo real — los developers verán el estado actualizado la próxima vez que ejecuten `/tasklist`.

---

### Cómo eliminar una Tarea

1. Abre el side panel de la tarea haciendo clic en la task card.
2. Haz clic en el botón **Eliminar** (delete).
3. Confirma la eliminación en el diálogo de confirmación.

> **Caution:** Eliminar una tarea es permanente y no se puede deshacer. La tarea también se eliminará de las tres listas de resultados de engines en cualquier sesión abierta de análisis de duplicados.

---

## Agent — AI-Powered Automation

La página **Agent** (`/agent`) centraliza las capacidades de planificación y analítica con AI. Ofrece dos herramientas:

| Tool | Qué hace |
|---|---|
| **Generar tareas** | Usa AI para sugerir un conjunto de tareas para un proyecto con base en un número objetivo de horas |
| **Análisis de tareas duplicadas** | Ejecuta tres AI engines en paralelo para detectar tareas potencialmente duplicadas en un proyecto |

---

### Cómo generar Tareas automáticamente con AI

1. Navega a **Agent** desde la barra de navegación.
2. Haz clic en la card **Generar tareas**.
3. Se abre un modal selector de proyecto. Selecciona el proyecto objetivo e ingresa las horas objetivo.
4. Haz clic en **Continuar**.
5. Irás a la página **Agent · Generar tareas**. Espera mientras AI genera sugerencias — aparecerán un indicador de carga y el mensaje "Generando sugerencias...". Permanece en esta página hasta que termine.
6. Al completar, aparece un tablero de tareas sugeridas (consulta [Cómo revisar, editar y aprobar sugerencias de Tareas de AI](#cómo-revisar-editar-y-aprobar-sugerencias-de-tareas-de-ai)).

> **Pro Tip:** Esta función funciona mejor cuando el AI Agent tiene contexto sobre las metas, requisitos y documentación de tu proyecto. Sube y elimina estos attachments desde la [página Proyectos.](#cómo-administrar-attachments-de-proyecto)

> **Caution:** No navegues fuera de la página mientras se generan las sugerencias — salir interrumpirá el proceso.

---

### Cómo revisar, editar y aprobar sugerencias de Tareas de AI

Cada tarea generada por AI aparece como una card en el tablero de sugerencias. Para cada card puedes:

**Aceptar una sugerencia tal como está:**
1. Toca el botón de aprobación en la card para marcarla como **Approved**.

**Editar una sugerencia antes de aprobarla:**
1. Haz clic en el icono **Edit** (pencil) de la card.
2. Se abre un modal de aprobación donde puedes modificar:
   - **Title**
   - **Description**
   - **Priority** (Alta / Media / Baja)
   - **Sprint** (selecciona de los sprints existentes del proyecto)
   - **Fecha límite** (due date)
3. Haz clic en **Guardar** en el modal.

**Rechazar una sugerencia:**
1. Haz clic en el botón de rechazo en la card para marcarla como **Rejected**.

**Aplicar todas las decisiones:**
1. Después de revisar todas las cards, haz clic en **Guardar Cambios** en el header de la página.
2. Un mensaje de éxito confirma cuántas tareas se crearon.

> **Pro Tip:** El botón **Guardar Cambios** está deshabilitado hasta que al menos una tarea esté marcada como approved. Debes aprobar al menos una sugerencia antes de guardar.

> **Caution:** Hacer clic en **Guardar Cambios** es permanente — las tareas aprobadas se crean inmediatamente en el proyecto y aparecerán en el tablero Kanban de **Tareas**.

---

### Cómo ejecutar un análisis de Tareas duplicadas

1. Navega a **Agent** desde la barra de navegación.
2. Haz clic en la card **Análisis de tareas duplicadas**.
3. Se abre un modal selector de proyecto. Selecciona el proyecto objetivo y, opcionalmente, ajusta el **similarity threshold** (predeterminado: 0.88 — valores más altos requieren mayor similitud para marcar un par como duplicado).
4. Haz clic en **Analizar**.
5. Irás a la página de resultados de análisis de duplicados. Una barra de progreso e indicadores de pasos muestran el avance del pipeline:

| Step | Qué ocurre |
|---|---|
| 1. Generating semantic embeddings | AI convierte el texto de cada tarea en un vector numérico |
| 2. Waiting for semantic embeddings | El sistema confirma que todos los embeddings están listos |
| 3. Preparing Oracle vectors | Los embeddings se indexan en Oracle AI Vector Search |
| 4. Confirming Oracle Vector Search | El sistema verifica que el índice vectorial esté listo |
| 5. Running detection engines | Los tres engines se ejecutan simultáneamente |

6. Permanece en la página hasta que el indicador de estado muestre **COMPLETADO**.

> **Caution:** No navegues fuera durante el pipeline. El proceso puede tomar 15–60 segundos dependiendo del tamaño del proyecto.

---

### Cómo revisar y eliminar Tareas duplicadas

Una vez que el pipeline termina, los resultados se muestran en tres paneles colapsables — uno por detection engine:

| Engine | Método |
|---|---|
| **LLM Directo** | Análisis directo por un language model |
| **Python Embeddings** | Comparación usando similitud de vectores semánticos |
| **Oracle AI Vector Search** | Búsqueda nativa de similitud vectorial en Oracle Database |

Cada panel lista **pares** duplicados (Task A y Task B) con una puntuación de similitud. El panel de Oracle Vector Search también muestra un valor de distancia.

**Para colapsar o expandir un panel:** haz clic en el header del panel.

**Para eliminar una tarea duplicada:**
1. En cualquier panel de resultados, encuentra el par que quieres resolver.
2. Haz clic en el botón **Eliminar** junto a Task A o Task B (la que sea redundante).
3. Aparece un diálogo de confirmación que muestra el título de la tarea.
4. Haz clic en **Eliminar** para confirmar.
5. La tarea eliminada se remueve automáticamente de las tres listas de resultados de engines al mismo tiempo.

> **Caution:** No puedes eliminar una tarea que tenga el estado **Completada**. El sistema mostrará un error — resuelve el estado primero desde la página **Tareas** si es necesario.

---

## Proyectos — Project Management

La página **Proyectos** (`/proyectos`) muestra todos los proyectos de tus equipos en una cuadrícula de cards.

### Cómo explorar y filtrar Proyectos

1. Navega a **Proyectos** desde la barra de navegación.
2. Cada card muestra el nombre del proyecto, equipo, progreso general y proporción de completitud de tareas (tareas completadas / tareas totales).
3. Para filtrar por equipo, usa el dropdown **Equipo** en la parte superior de la página. Selecciona un equipo específico o déjalo vacío para mostrar todos.
4. Tu selección de filtro de equipo se persiste entre sesiones.

---

### Cómo crear un nuevo Proyecto

> **Required role:** Manager

1. En la página **Proyectos**, haz clic en **+ Nuevo proyecto**.
2. Completa el formulario:
   - **Nombre** — nombre del proyecto (requerido)
   - **Descripción** — descripción opcional
   - **Fecha inicio** — fecha y hora de inicio
   - **Fecha fin** — fecha y hora de fin
3. El proyecto se vincula automáticamente al equipo actualmente seleccionado en el filtro de equipo.
4. Haz clic en **Crear proyecto**.
5. La nueva project card aparece en la cuadrícula.

> **Caution:** El botón **+ Nuevo proyecto** está deshabilitado si todavía no existe ningún equipo. Crea un equipo primero desde la [página Equipos](#cómo-crear-un-nuevo-equipo).

---

### Cómo ver el KPI Dashboard de un Proyecto

1. Haz clic en una project card para abrir su dashboard (`/proyectos/:projectId`).
2. El header muestra el nombre del proyecto, el equipo vinculado y una barra de progreso general.
3. La **ProyectosDashboardSection** debajo muestra KPIs a nivel sprint y métricas de performance del equipo para ese proyecto específico.

---

### Cómo administrar Attachments de Proyecto

> **Required role:** Manager

1. Abre el dashboard de un proyecto y haz clic en Editar proyecto.
2. En el side panel, desplázate hacia abajo hasta la sección Attachments.
3. Para subir un archivo, haz clic en el upload box (o arrastra un archivo sobre él). La carga comienza automáticamente — no se requiere paso extra de confirmación.
    - Formatos aceptados: PDF, imágenes, Word documents (.doc / .docx)
    - Tamaño máximo de archivo: 20 MB
4. Una vez cargado, el archivo aparece en la lista de documents con su nombre y tamaño. Haz clic en el enlace del filename para abrirlo en una pestaña nueva.
5. Para eliminar un attachment, haz clic en el icono rojo de trash junto al archivo. Aparecerá un diálogo de confirmación — haz clic en Delete para confirmar.

> **Caution:** Eliminar un attachment es permanente y no se puede deshacer.

---

### Cómo editar o eliminar un Proyecto

> **Required role:** Manager

1. Abre el dashboard del proyecto haciendo clic en su card.
2. Haz clic en **Editar proyecto** en la esquina superior derecha.
3. Se abre un side panel con campos editables: nombre, descripción, fecha de inicio, fecha de fin.
4. Haz tus cambios y haz clic en **Guardar**.
5. Para eliminar el proyecto, haz clic en **Eliminar proyecto** en la parte inferior del side panel y confirma.

> **Caution:** Eliminar un proyecto es permanente. Todas las tareas asociadas y datos de sprint también se eliminan.

---

## Equipos — Team Management

La página **Equipos** (`/equipos`) administra los equipos que poseen tus proyectos.

### Cómo explorar tus Equipos

1. Navega a **Equipos** desde la barra de navegación.
2. Tres summary cards en la parte superior muestran: **Total teams**, **Total members**, **Total projects**.
3. Una tabla debajo lista cada equipo con su nombre, número de miembros y número de proyectos vinculados.
4. Haz clic en cualquier fila para abrir la página de detalle del equipo.

---

### Cómo crear un nuevo Equipo

> **Required role:** Manager

1. En la página **Equipos**, haz clic en **+ Nuevo equipo**.
2. Completa:
   - **Nombre** — nombre del equipo (requerido)
   - **Descripción** — descripción opcional
   - **Owner** — selecciona el team owner desde el dropdown (requerido)
3. Haz clic en **Guardar**.
4. El nuevo equipo aparece en la tabla.

---

### Cómo agregar o quitar un miembro de Equipo

1. Haz clic en una fila de equipo para abrir su página de detalle (`/equipos/:teamId`).
2. En la card **Members**:
   - Para **add a member**: haz clic en **+ Agregar miembro**, selecciona un usuario desde el dropdown y haz clic en **Agregar**.
   - Para **remove a member**: haz clic en el icono de quitar (✕) junto a su nombre. La acción surte efecto inmediatamente.

> **Caution:** Quitar un miembro de un equipo no lo desasigna de tareas existentes. Revisa las asignaciones de tareas en **Tareas** después de quitar un miembro.

---

### Cómo editar la Description de un Equipo

1. Abre la página de detalle del equipo.
2. En la card **Description**, haz clic dentro del área de texto y actualiza el texto.
3. Haz clic en **Guardar descripción**.
4. Aparece una notificación de confirmación en la esquina inferior derecha de la pantalla.

---

## Telegram Bot — Developer Interface

El Telegram bot es la interfaz principal para que developers gestionen tareas desde su teléfono o cliente Telegram de desktop.

### Cómo conectar tu cuenta de Telegram

Antes de empezar, confirma con tu Manager que tu **Telegram ID** se haya ingresado en tu perfil de usuario en el web dashboard.

1. Abre **Telegram** y busca el nombre del bot proporcionado por tu Manager.
2. Abre el chat del bot.
3. Toca **Start** o escribe `/start` y presiona [Send].
4. Si tu ID está registrado, el bot responde con un mensaje de bienvenida y muestra los botones del menú principal.
5. Si ves `Your account is not linked`, contacta a tu Manager para verificar tu Telegram ID.

---

### Cómo seleccionar tu Proyecto activo

Debes seleccionar un proyecto antes de usar cualquier comando de tareas.

1. Toca **Select Project** en el menú, o escribe `/project` y presiona [Send].
2. El bot lista todos los proyectos a los que estás asignado.
3. Toca el nombre del proyecto en el que quieres trabajar.
4. El bot confirma la selección.

> **Caution:** Todos los comandos de tareas aplican solo al proyecto activo. Si cambias de proyecto, ejecuta `/tasklist` de nuevo para ver la lista de tareas correcta.

---

### Cómo ver y actualizar tus Tareas

1. Toca **List All Tasks**, o escribe `/tasklist` y presiona [Send].
2. El bot devuelve tus tareas asignadas para el proyecto activo, mostrando título, estado y fecha límite.
3. Toca una tarea para ver opciones de detalle.
4. Toca el botón de estado que coincida con tu avance:
   - **IN PROGRESS** — ya empezaste la tarea
   - **DONE** — la tarea está completa
   - **CANCELLED** — la tarea no se completará
5. El bot confirma el cambio. El tablero Kanban en el web dashboard se actualiza en tiempo real.

> **Pro Tip:** Si un botón de estado no responde, escribe `/start` para refrescar tu sesión e intenta de nuevo.

> **Caution:** Los cambios de estado mediante el bot no se pueden deshacer mediante el bot. Pídele a tu Manager que corrija un estado equivocado desde la página **Tareas**.

---

### Cómo agregar una Tarea mediante Telegram

1. Selecciona primero un proyecto (consulta [Cómo seleccionar tu Proyecto activo](#cómo-seleccionar-tu-proyecto-activo)).
2. Escribe `/addtask` y presiona [Send].
3. Sigue los prompts del bot:
   1. Ingresa el **task title** y presiona [Send].
   2. Ingresa la **due date** en el formato que el bot especifica.
   3. Confirma los detalles cuando se te solicite.
4. La tarea se crea en el proyecto activo y se te asigna a ti.

---

### Referencia de comandos del Bot

| Command / Button | Qué hace |
|---|---|
| `/start` | Abre el bot y muestra el menú principal. |
| `/hide` | Oculta el teclado del menú. Escribe `/start` para mostrarlo de nuevo. |
| `/project` | Muestra el selector de proyecto. |
| `/tasklist` | Lista tus tareas en el proyecto activo. |
| `/addtask` | Inicia el flujo para crear una nueva tarea. |
| **Select Project** | Botón de menú — igual que `/project`. |
| **List All Tasks** | Botón de menú — igual que `/tasklist`. |
| **IN PROGRESS** | Establece el estado de la tarea en In Progress. |
| **DONE** | Establece el estado de la tarea en Done. |
| **CANCELLED** | Establece el estado de la tarea en Cancelled. |

---

## Solución de problemas y errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Telegram bot responde `Your account is not linked` | Falta el Telegram ID o es incorrecto en el web dashboard | Pídele a tu Manager que corrija el **Telegram ID** en tu perfil de usuario. |
| Telegram bot no responde a `/start` | Nombre de bot incorrecto, o backend offline | Verifica el nombre del bot con tu Manager. Si es correcto, contacta a tu system administrator — el backend service puede estar caído. |
| Telegram responde `No projects were found for your user` | No estás asignado a ningún proyecto | Pídele a tu Manager que te agregue a un proyecto o equipo. |
| Telegram responde `No active project selected` | No has seleccionado un proyecto en esta sesión | Ejecuta `/project` o toca **Select Project** antes de emitir otros comandos. |
| Una tarea recién creada no aparece en la lista del bot | Lista de tareas desactualizada, o proyecto activo incorrecto | Ejecuta `/tasklist` para refrescar. Ejecuta `/project` para confirmar que estás en el proyecto correcto. |
| El botón **IN PROGRESS** / **DONE** no tiene efecto | Sesión expirada | Escribe `/start` para reiniciar la sesión, volver a listar tus tareas e intentar de nuevo. |
| Manager no puede ver el cambio de estado de un developer | Retraso de sincronización en tiempo real | Recarga la página **Tareas** en el navegador. |
| **Agent · Generar tareas** se queda cargando indefinidamente | El AI service está lento o temporalmente no disponible | Permanece en la página y espera hasta 60 segundos. Si no aparece nada, regresa e intenta de nuevo. |
| La detección de duplicados muestra `Error` en un engine panel | Ese engine falló — los otros aún pueden tener resultados | Los otros dos engine panels son independientes. Revisa sus resultados y vuelve a ejecutar el pipeline desde **Agent** si es necesario. |
| Error `No se puede eliminar una tarea completada` al eliminar desde resultados de duplicados | El estado de la tarea es **Completada** | Cambia el estado de la tarea a algo distinto de Completada desde la página **Tareas** y vuelve a intentar. |
| El botón **+ Nuevo proyecto** está deshabilitado | No existen equipos, o tu rol no es Manager | Crea un equipo primero desde **Equipo**, o contacta a tu administrador para verificar tu rol. |
| El web dashboard muestra pantalla en blanco o spinner infinito | Problema de cache del navegador, o API inalcanzable | Presiona [Ctrl]+[Shift]+[Delete] (Windows) o [Cmd]+[Shift]+[Delete] (macOS), limpia el cache y recarga. Si el problema persiste, contacta a tu system administrator. |

---

## Información de versión y entorno

| Ítem | Detalles |
|---|---|
| Guide version | Sprint 3 — Module 2 (May 2026) |
| Application release | Oracle Java Bot v1.0 |
| Backend | Spring Boot 3 · Java 21 |
| Frontend | React 18 · TypeScript · Vite |
| AI Service | Python 3 · FastAPI |
| Database | Oracle Autonomous Database (ATP) |
| Supported browsers | Chrome 124+, Firefox 125+, Edge 124+ |
| Telegram app | Cualquier release actual (Android, iOS, Desktop) |
| Last validated | May 2026 — Sprint 3 acceptance testing |

---

## Feedback

¿Esta guía fue útil?

- Abre un issue en el project repository y etiquétalo como **`docs`**.
- Para soporte urgente, contacta directamente a tu Manager o system administrator.

---

*Oracle Java Bot — User Guide · Sprint 3, Module 2 · Team 43*
*Alfredo Carmona · Clay Gutiérrez · Emilio Hernández · Luis Díaz*
