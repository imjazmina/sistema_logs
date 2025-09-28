# 📝 Sistema de Logs con Flask y SQLite

Este proyecto implementa un sistema de gestión de **logs** como microservicio.  
Permite registrar eventos, consultarlos y filtrarlos por diferentes criterios.

---

## ⚙️ Tecnologías utilizadas
- Python 3.x  
- Flask (framework web)  
- SQLite (base de datos ligera)  

---

## 📌 Funcionalidades
- **Registro de logs**: almacenar eventos en la base de datos.  
- **Listado de logs**: obtener todos los registros guardados.  
- **Filtrado**: consultar logs por severidad, servicio o rango de fechas.  
- **Persistencia**: uso de SQLite para mantener la información.  

---

## 📂 Estructura del proyecto

```bash
logs_service/
├── app.py          # Servicio principal de Flask
├── logs.db         # Base de datos SQLite (se crea automáticamente)
└── README.md
````

---

## ▶️ Cómo ejecutar el proyecto

1. Clonar el repositorio o copiar la carpeta del servicio.
2. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```
3. Instalar dependencias:

   ```bash
   pip install flask
   ```
4. Ejecutar el servicio:

   ```bash
   python app.py
   ```
5. El servidor se abrirá en:

   ```
   http://127.0.0.1:5000
   ```

---

## 📮 Endpoints principales

### ➤ Registrar un log

**POST** `/logs`

```json
{
  "service": "auth",
  "severity": "error",
  "message": "Usuario no autorizado"
}
```

### ➤ Listar todos los logs

**GET** `/logs`

### ➤ Filtrar por severidad

**GET** `/logs/severity/<nivel>`
Ejemplo:

```
/logs/severity/error
```

### ➤ Filtrar por servicio

**GET** `/logs/service/<nombre_servicio>`
Ejemplo:

```
/logs/service/auth
```

### ➤ Filtrar por fecha

**GET** `/logs?from=2025-09-01&to=2025-09-10`

``
