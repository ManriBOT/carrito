# RED ESTAMPACION

Plataforma de comercio electrónico desarrollada con Django para la venta de camisas personalizadas. Proyecto académico profesional que implementa una arquitectura de 3 capas, 12 capas de seguridad OWASP y diseño responsive mobile-first.

---

## Desglose Arquitectónico

### Arquitectura de 3 Capas

| Capa | Ubicación | Responsabilidad |
|------|-----------|-----------------|
| **Presentación** | `views.py`, `templates/`, `static/` | Recibir peticiones HTTP, renderizar interfaces, gestionar respuestas |
| **Lógica de Negocio** | `services.py`, `forms.py` | Reglas de negocio del carrito, cálculos de subtotal, validaciones |
| **Acceso a Datos** | `models.py` | ORM nativo de Django para interacción con base de datos SQLite |

Las vistas (`views.py`) **nunca** acceden directamente a los modelos. La comunicación sigue la ruta: `views → services → models`.

---

## Matriz de Seguridad (12 Capas vs OWASP Top 10)

| # | Capa de Seguridad | OWASP Relacionado | Implementación |
|---|-------------------|-------------------|----------------|
| 1 | **CSRF** | A01:2021-Broken Access Control | Middleware `CsrfViewMiddleware` + `{% csrf_token %}` en formularios |
| 2 | **XSS** | A03:2021-Injection | Auto-escape del motor de plantillas Django |
| 3 | **SQL Injection** | A03:2021-Injection | ORM parametrizado exclusivamente, prohibido SQL raw |
| 4 | **Hash de Contraseñas** | A02:2021-Crypto Failures | PBKDF2 con SHA256 (`AUTH_PASSWORD_VALIDATORS`) |
| 5 | **Sesiones Seguras** | A01:2021-Broken Access Control | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'` |
| 6 | **HTTPS** | A02:2021-Crypto Failures | `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` condicionales |
| 7 | **Clickjacking** | A01:2021-Broken Access Control | `XFrameOptionsMiddleware` con cabecera `DENY` |
| 8 | **Host Validation** | A01:2021-Broken Access Control | `ALLOWED_HOSTS` restringido vía `.env` |
| 9 | **RBAC** | A01:2021-Broken Access Control | `@login_required` + carritos aislados por usuario (`OneToOneField`) |
| 10 | **Variables de Entorno** | A05:2021-Security Misconfiguration | `SECRET_KEY` y credenciales extraídas de `.env` con `python-dotenv` |
| 11 | **Rate Limiting** | A04:2021-Insecure Design | Simulación de control de tasa en endpoint de autenticación |
| 12 | **Input Sanitization** | A03:2021-Injection | Validación exhaustiva en `forms.py` (tipos, longitudes, formatos) |

---

## Especificaciones de Identidad Visual

### Paleta de Colores (Estricta)

| Color | Código Hex | Uso |
|-------|-----------|-----|
| Rojo Corporativo | `#D32F2F` | Botones primarios, títulos, acentos |
| Blanco | `#FFFFFF` | Fondos, tarjetas, contraste |
| Negro | `#1A1A1A` | Textos, bordes, header, footer |

**Queda prohibido** el uso de degradados o cualquier color fuera de esta tríada, incluso en alertas de éxito o error.

### Diseño Responsive

- **Mobile-First**: Diseñado desde 320px hacia arriba
- **Breakpoints**: 600px (tablet) y 900px (desktop)
- Metodología: CSS Grid con `grid-template-columns` adaptable

---

## Árbol de Directorios

```
red_estampacion/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── tienda/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── services.py
│       ├── forms.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── templates/
│       │   └── tienda/
│       │       ├── base.html
│       │       ├── login.html
│       │       ├── catalogo.html
│       │       └── carrito.html
│       └── static/
│           ├── css/
│           │   └── styles.css
│           └── js/
│               └── main.js
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Guía de Instalación Local

### Requisitos previos

- Python 3.10 o superior
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/ManriBOT/carrito.git
cd carrito

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
# source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Editar el archivo .env con una SECRET_KEY segura
# SECRET_KEY=tu-clave-secreta-aqui
# DEBUG=True
# ALLOWED_HOSTS=127.0.0.1,localhost

# 5. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Ejecutar servidor de desarrollo
python manage.py runserver
```

Acceder a `http://127.0.0.1:8000/` para comenzar.

---

## Licencia

Proyecto académico - RED ESTAMPACION
