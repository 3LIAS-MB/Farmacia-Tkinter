# 🏥 Sistema de Gestión de Farmacia

Sistema de escritorio desarrollado en Python con Tkinter para la gestión integral de una farmacia, incluyendo control de inventario, ventas y administración de usuarios.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#️-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Arquitectura](#️-arquitectura)
- [Base de Datos](#️-base-de-datos)
- [Seguridad](#-seguridad)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## ✨ Características

### Para Clientes

- 🛒 **Catálogo de productos** con búsqueda avanzada
- 🛍️ **Carrito de compras** interactivo
- 💳 **Múltiples métodos de pago** (Contado, Débito, Crédito)
- 📍 **Selección de sucursal** más cercana
- 🧾 **Generación de recibos** de compra

### Para Administradores

- 👥 **Gestión completa de usuarios** (CRUD)
- 📦 **Gestión de productos** e inventario
- 🏢 **Administración de sucursales**
- 📊 **Reportes de ventas**
- 🔐 **Control de accesos** por roles

---

## 🛠️ Tecnologías

- **Lenguaje:** Python 3.x
- **GUI:** Tkinter + ttk (tema clam)
- **Base de Datos:** SQLite 3
- **Seguridad:** SHA256 para encriptación de contraseñas
- **Arquitectura:** MVC (Model-View-Controller)

---

## 📦 Requisitos Previos

- Python 3.x instalado
- Tkinter (incluido en instalación estándar de Python)
- Sistema operativo: Windows, macOS, o Linux

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/3LIAS-MB/Farmacia-Tkinter.git
cd Farmacia-Tkinter
```

### 2. Verificar instalación de Python

```bash
python --version
```

### 3. Ejecutar la aplicación

```bash
cd farmacia_ecommerce
python main.py
```

> **Nota:** La base de datos `farmacia.db` se creará automáticamente en la primera ejecución.

---

## 💻 Uso

### Inicio de Sesión

Al ejecutar `main.py`, se abrirá la ventana de inicio de sesión:

**Usuarios de prueba:**

- **Cliente:** `cliente1` / `password123`
- **Admin:** `admin` / `admin123`

### Flujo de Compra (Cliente)

1. Iniciar sesión como cliente
2. Navegar al catálogo de productos
3. Agregar productos al carrito
4. Seleccionar método de pago
5. Confirmar compra y obtener recibo

### Panel de Administración

1. Iniciar sesión como administrador
2. Acceder a módulos de gestión:
   - **Usuarios:** CRUD completo
   - **Productos:** Gestión de inventario
   - **Sucursales:** Administración de ubicaciones

---

## 📁 Estructura del Proyecto

```
farmacia_ecommerce/
├── config/
│   └── database.py          # Configuración de SQLite
├── models/
│   ├── usuario.py           # Modelo de Usuario
│   ├── producto.py          # Modelo de Producto
│   ├── venta.py             # Modelo de Venta
│   └── sucursal.py          # Modelo de Sucursal
├── gui/
│   ├── admin/
│   │   ├── gestion_usuarios.py
│   │   ├── gestion_productos.py
│   │   └── gestion_sucursales.py
│   └── cliente/
│       ├── consulta_productos.py
│       └── proceso_compra.py
├── utils/
│   └── validaciones.py      # Funciones de validación
├── farmacia.db              # Base de datos SQLite
└── main.py                  # Punto de entrada
```

---

## 🏗️ Arquitectura

El sistema sigue el patrón **MVC (Model-View-Controller)**:

- **Models** (`models/`): Lógica de negocio y acceso a datos
- **Views** (`gui/`): Interfaces gráficas con Tkinter
- **Controller**: Integrado en `main.py`

### Gestión de Base de Datos

El sistema utiliza `DatabaseManager` para centralizar todas las operaciones de base de datos, garantizando:

- ✅ Conexiones seguras
- ✅ Transacciones ACID
- ✅ Manejo de errores consistente

---

## 🗄️ Base de Datos

### Esquema Principal

#### Tabla: `usuarios`

| Campo    | Tipo                | Descripción         |
| -------- | ------------------- | ------------------- |
| id       | INTEGER PRIMARY KEY | Identificador único |
| username | TEXT UNIQUE         | Nombre de usuario   |
| password | TEXT                | Contraseña (SHA256) |
| rol      | TEXT                | 'admin' o 'cliente' |

#### Tabla: `productos`

| Campo       | Tipo                | Descripción              |
| ----------- | ------------------- | ------------------------ |
| id          | INTEGER PRIMARY KEY | Identificador único      |
| nombre      | TEXT                | Nombre del producto      |
| descripcion | TEXT                | Descripción del producto |
| precio      | REAL                | Precio unitario          |
| stock       | INTEGER             | Cantidad disponible      |

#### Tabla: `ventas`

| Campo       | Tipo                | Descripción              |
| ----------- | ------------------- | ------------------------ |
| id          | INTEGER PRIMARY KEY | Identificador único      |
| usuario_id  | INTEGER             | ID del usuario           |
| fecha       | TEXT                | Fecha de la venta        |
| total       | REAL                | Monto total              |
| metodo_pago | TEXT                | Método de pago utilizado |

#### Tabla: `sucursales`

| Campo     | Tipo                | Descripción           |
| --------- | ------------------- | --------------------- |
| id        | INTEGER PRIMARY KEY | Identificador único   |
| nombre    | TEXT                | Nombre de la sucursal |
| direccion | TEXT                | Dirección física      |
| telefono  | TEXT                | Número de contacto    |

---

## 🔒 Seguridad

- 🔐 Contraseñas encriptadas con **SHA256**
- ✅ Validación de entrada en todos los formularios
- 👮 Control de acceso basado en **roles**
- 🛡️ Prevención de inyección SQL mediante **consultas parametrizadas**

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible públicamente para uso, modificación y distribución libre.

---

## 👥 Autores

- **Mamaní Elías Braulio** - [3LIAS-MB](https://github.com/3LIAS-MB)

---

## 📧 Contacto

Para preguntas o sugerencias:

- **Email:** [eliasss.mb@gmail.com]
- **GitHub:** [@3LIAS-MB](https://github.com/3LIAS-MB)
- **Issues:** [Reportar un problema](https://github.com/3LIAS-MB/Farmacia-Tkinter/issues)
