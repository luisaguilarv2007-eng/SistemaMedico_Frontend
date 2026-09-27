# IUJO SaludConnect - Sistema Administrativo y de Gestión Médica

## Descripción del Software y Alcance del Negocio
IUJO SaludConnect es un sistema centralizado diseñado para la gestión operativa y clínica de centros de salud y ambulatorios. Su objetivo principal es mantener la operatividad local (offline) garantizando que los registros, la facturación y el procesamiento de resultados funcionen de manera continua en la red LAN del recinto.

## Módulos Principales
El software abarca cuatro áreas operativas clave:
* **Módulo A (Autenticación y Perfiles):** Control de acceso seguro y diferenciado para perfiles como Administrador, Médico, Laboratorio y Caja.
* **Módulo B (Registro Centralizado):** Ficha única de pacientes, consultas en tiempo real y registro automático en una bitácora de auditoría.
* **Módulo C (Gestión de Estudios Clínicos):** Registro de órdenes médicas, validación rigurosa de resultados por profesionales y portal de revisión para médicos.
* **Módulo D (Facturación y Cobranza):** Generación de presupuestos, emisión de facturas, soporte para múltiples métodos de pago y control estricto de validación previa al procesamiento de estudios.

## Tecnologías Utilizadas (Stack Frontend)
El diseño de la interfaz ha sido estructurado utilizando tecnologías web estándar, garantizando rendimiento y compatibilidad nativa en navegadores web:
* **HTML5:** Estructura semántica, destacando el uso de la API nativa

* **CSS3 (Vanilla):** Arquitectura de estilos responsiva apoyada en un "Living Style Guide". Utiliza variables globales (`:root`) para aplicar la paleta oficial (Obsidian Black, Ruby Crimson, Deep Maroon, etc.) a lo largo de todo el sistema.
* **JavaScript (Vanilla JS):** Lógica interactiva ligera, sin frameworks pesados, encargada de controlar el menú hamburguesa responsivo y las notificaciones temporizadas (Toasts).

## Modelo de Base de Datos
La estructura relacional del sistema integra diversas tablas para soportar toda la operación clínica y administrativa, conectando entidades esenciales como: pacientes, usuarios, catálogo de servicios, órdenes con sus respectivos detalles, documentos de facturación, pagos recibidos y la bitácora de auditoría.

## Datos Académicos e Integrantes
**Institución:** Instituto Universitario Jesús Obrero (IUJO)

**Asignatura:** Análisis y Diseño de Sistemas (ADS-433) **Sección A**
    
**Estudiante:**
* Kenneth Espinoza - C.I: 30.753.863 
* Luisangel Aguilar - C.I: 31.960926
* Alianny Rodriguez - C.I: 29.915.912
* Reibert Alzuru - C.I: 32.774.319
