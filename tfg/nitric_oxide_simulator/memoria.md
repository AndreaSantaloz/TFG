# TRABAJO DE FIN DE GRADO - ESTRUCTURA COMPLETA

## ÍNDICE GENERAL

### 1. INTRODUCCIÓN
- 1.1. Motivación y Contexto del Proyecto
  - 1.1.1. Problemática actual
  - 1.1.2. Oportunidad de mejora
- 1.2. Objetivos del Proyecto
  - 1.2.1. Objetivo General
  - 1.2.2. Objetivos Específicos
- 1.3. Alcance y Limitaciones
  - 1.3.1. Funcionalidades incluidas
  - 1.3.2. Funcionalidades excluidas
- 1.4. Metodología de Trabajo
  - 1.4.1. Metodología ágil (SCRUM/Kanban)
  - 1.4.2. Herramientas de gestión
- 1.5. Estructura del Documento

---

### 2. DESCRIPCIÓN DE LA APLICACIÓN Y OBJETIVOS
- 2.1. Descripción General del Sistema
  - 2.1.1. Propósito de la aplicación
  - 2.1.2. Perfiles de usuario
- 2.2. Requisitos Funcionales (RF)
  - 2.2.1. Gestión de usuarios
  - 2.2.2. Gestión de [entidad principal]
  - 2.2.3. Generación de informes
- 2.3. Requisitos No Funcionales (RNF)
  - 2.3.1. Usabilidad
  - 2.3.2. Rendimiento
  - 2.3.3. Seguridad
  - 2.3.4. Disponibilidad y portabilidad
- 2.4. Diagramas de Casos de Uso
  - 2.4.1. Diagrama general
  - 2.4.2. Especificación de casos de uso

---

### 3. DISEÑO DE LA SOLUCIÓN
- 3.1. Introducción al Diseño
- 3.2. Diseño Arquitectónico
  - 3.2.1. Justificación de la arquitectura
- 3.3. Diseño de la Base de Datos
  - 3.3.1. Diagrama Entidad-Relación (MER)
  - 3.3.2. Diccionario de datos
  - 3.3.3. Relaciones entre tablas
- 3.4. Diseño de la Interfaz de Usuario
  - 3.4.1. Boceto de la página de inicio
  - 3.4.2. Boceto del formulario de registro/login
  - 3.4.3. Boceto del dashboard
- 3.5. Diseño de la Navegación (Sitemap)

---

### 4. ARQUITECTURA SOFTWARE
- 4.1. Modelo Cliente-Servidor
  - 4.1.1. Definición y justificación
  - 4.1.2. Diagrama de despliegue
- 4.2. Patrón Arquitectónico MVT (Model-View-Template)
  - 4.2.1. Definición del patrón MVT
  - 4.2.2. Comparativa: MVC vs MVT vs MVP
  - 4.2.3. Ventajas e inconvenientes del MVT
- 4.3. Descripción Detallada de las Capas MVT
  - 4.3.1. Capa Template (Presentación)
  - 4.3.2. Capa View (Lógica de negocio)
  - 4.3.3. Capa Model (Datos y ORM)
- 4.4. Flujo de Petición-Respuesta (El "encaje")
  - 4.4.1. Explicación paso a paso
  - 4.4.2. Diagrama de secuencia
- 4.5. Componentes Adicionales
  - 4.5.1. Middleware
  - 4.5.2. Django Admin
  - 4.5.3. Enrutador de URLs (urls.py)

---

### 5. MODELO DE DATOS
- 5.1. Introducción a la Persistencia
- 5.2. Tecnología de Base de Datos Seleccionada
  - 5.2.1. Justificación de la BBDD elegida
  - 5.2.2. Alternativas descartadas
- 5.3. Modelo Lógico de Datos
- 5.4. Implementación del ORM en Django
  - 5.4.1. Definición de las clases Model
  - 5.4.2. Relaciones (ForeignKey, ManyToMany)
  - 5.4.3. Métodos personalizados
- 5.5. Migraciones y Versionado
  - 5.5.1. Comandos makemigrations y migrate
  - 5.5.2. Gestión de cambios en el esquema

---

### 6. DESARROLLO E IMPLEMENTACIÓN
- 6.1. Entorno de Desarrollo
  - 6.1.1. Hardware y software utilizado
  - 6.1.2. Creación del entorno virtual
  - 6.1.3. Instalación de dependencias
- 6.2. Estructura de Carpetas del Proyecto
  - 6.2.1. Árbol de directorios
  - 6.2.2. Explicación de archivos clave
- 6.3. Implementación del Modelo (Models)
  - 6.3.1. Código de los modelos principales
  - 6.3.2. Registro en Django Admin
- 6.4. Implementación de las Vistas (Views)
  - 6.4.1. FBV vs CBV
  - 6.4.2. Implementación de vistas principales
- 6.5. Implementación de las Plantillas (Templates)
  - 6.5.1. Herencia de plantillas
  - 6.5.2. Implementación con Bootstrap
- 6.6. Enrutamiento (URLs)
  - 6.6.1. Definición de patrones de URL
  - 6.6.2. Nombrado y reversión de URLs
- 6.7. Gestión de Formularios
  - 6.7.1. Formularios Django (forms.py)
  - 6.7.2. Validación de datos
- 6.8. Seguridad Implementada
  - 6.8.1. Autenticación de usuarios
  - 6.8.2. Protección CSRF y XSS
  - 6.8.3. Control de acceso por roles

---

### 7. INTERFACES Y RESULTADOS
- 7.1. Interfaz de Usuario
  - 7.1.1. Pantalla de inicio / Landing page
  - 7.1.2. Pantalla de registro
  - 7.1.3. Pantalla de login
  - 7.1.4. Pantalla principal / Dashboard
  - 7.1.5. Pantalla de gestión de [entidad]
  - 7.1.6. Pantalla de informes
- 7.2. Pruebas y Verificación
  - 7.2.1. Pruebas unitarias
  - 7.2.2. Tabla de casos de prueba
  - 7.2.3. Pruebas de usabilidad
- 7.3. Despliegue
  - 7.3.1. Despliegue en servidor
  - 7.3.2. Instrucciones de instalación
  - 7.3.3. Manual de usuario básico

---

### 8. CONCLUSIONES Y TRABAJO FUTURO
- 8.1. Cumplimiento de Objetivos
  - 8.1.1. Objetivos alcanzados
  - 8.1.2. Objetivos no cumplidos
- 8.2. Dificultades Encontradas
  - 8.2.1. Problemas técnicos
  - 8.2.2. Problemas de organización
- 8.3. Valoración Personal (Aprendizaje)
- 8.4. Líneas de Trabajo Futuro
  - 8.4.1. Mejoras funcionales
  - 8.4.2. Mejoras técnicas
  - 8.4.3. Despliegue en producción

---

### BIBLIOGRAFÍA Y REFERENCIAS
- Libros
- Documentación oficial de Django
- Artículos académicos
- Recursos web

---

### ANEXOS
- Anexo A: Manual de Instalación
- Anexo B: Código Fuente (enlace GitHub)
- Anexo C: Glosario de Términos

---

## 📊 PLAN DE PÁGINAS POR CAPÍTULO

| Capítulo | Páginas |
|----------|---------|
| 1. Introducción | 5 |
| 2. Descripción y Objetivos | 6 |
| 3. Diseño | 8 |
| 4. Arquitectura | 8 |
| 5. Modelo de Datos | 6 |
| 6. Desarrollo | 12 |
| 7. Interfaces y Resultados | 8 |
| 8. Conclusiones | 5 |
| Bibliografía y Anexos | 6 |
| **TOTAL** | **~64 páginas** |

## 📝 GUÍA DE REDACCIÓN PARA TU TEXTO MVT

### Cómo distribuir tu texto en el Capítulo 4:

**4.2. Patrón Arquitectónico MVT**
- Define el patrón con tus palabras (3 párrafos ≈ 150-200 palabras)

**4.2.2. Comparativa MVC vs MVT vs MVP** (1 tabla + 2 párrafos)