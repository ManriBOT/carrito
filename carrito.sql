-- =====================================================
-- BASE DE DATOS: carrito
-- SISTEMA: RED ESTAMPACION - E-commerce
-- MOTOR: MySQL
-- =====================================================

CREATE DATABASE IF NOT EXISTS carrito
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE carrito;

-- =====================================================
-- TABLA: auth_user (Usuarios del sistema)
-- =====================================================
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6) NULL,
    is_superuser TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    date_joined DATETIME(6) NOT NULL,
    INDEX auth_user_username_idx (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: auth_group
-- =====================================================
CREATE TABLE IF NOT EXISTS auth_group (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: auth_group_permissions
-- =====================================================
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE KEY auth_group_permissions_group_id_permission_id_uniq (group_id, permission_id),
    CONSTRAINT auth_group_permissions_group_fk FOREIGN KEY (group_id) REFERENCES auth_group (id) ON DELETE CASCADE,
    CONSTRAINT auth_group_permissions_permission_fk FOREIGN KEY (permission_id) REFERENCES auth_permission (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: auth_permission
-- =====================================================
CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL,
    UNIQUE KEY auth_permission_content_type_id_codename_uniq (content_type_id, codename),
    CONSTRAINT auth_permission_content_type_fk FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: django_content_type
-- =====================================================
CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE KEY django_content_type_app_label_model_uniq (app_label, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: django_migrations
-- =====================================================
CREATE TABLE IF NOT EXISTS django_migrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: django_session
-- =====================================================
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data LONGTEXT NOT NULL,
    expire_date DATETIME(6) NOT NULL,
    INDEX django_session_expire_date_idx (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: django_admin_log
-- =====================================================
CREATE TABLE IF NOT EXISTS django_admin_log (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    action_time DATETIME(6) NOT NULL,
    object_id LONGTEXT NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL,
    change_message LONGTEXT NOT NULL,
    content_type_id INTEGER NULL,
    user_id INTEGER NOT NULL,
    INDEX django_admin_log_content_type_id_idx (content_type_id),
    INDEX django_admin_log_user_id_idx (user_id),
    CONSTRAINT django_admin_log_content_type_fk FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON DELETE SET NULL,
    CONSTRAINT django_admin_log_user_fk FOREIGN KEY (user_id) REFERENCES auth_user (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: tienda_producto (Catálogo de productos)
-- =====================================================
CREATE TABLE IF NOT EXISTS tienda_producto (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    color VARCHAR(20) NOT NULL,
    talla VARCHAR(5) NOT NULL,
    descripcion VARCHAR(500) NOT NULL DEFAULT '',
    precio DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado DATETIME(6) NOT NULL,
    actualizado DATETIME(6) NOT NULL,
    INDEX tienda_producto_activo_idx (activo),
    INDEX tienda_producto_creado_idx (creado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: tienda_carrito (Carritos por usuario)
-- =====================================================
CREATE TABLE IF NOT EXISTS tienda_carrito (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INTEGER NOT NULL UNIQUE,
    creado DATETIME(6) NOT NULL,
    actualizado DATETIME(6) NOT NULL,
    CONSTRAINT tienda_carrito_usuario_fk FOREIGN KEY (usuario_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    INDEX tienda_carrito_usuario_idx (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- TABLA: tienda_carritoitem (Items dentro del carrito)
-- =====================================================
CREATE TABLE IF NOT EXISTS tienda_carritoitem (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    carrito_id BIGINT NOT NULL,
    producto_id BIGINT NOT NULL,
    cantidad INTEGER UNSIGNED NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(8, 2) NOT NULL,
    UNIQUE KEY tienda_carritoitem_carrito_producto_uniq (carrito_id, producto_id),
    CONSTRAINT tienda_carritoitem_carrito_fk FOREIGN KEY (carrito_id) REFERENCES tienda_carrito (id) ON DELETE CASCADE,
    CONSTRAINT tienda_carritoitem_producto_fk FOREIGN KEY (producto_id) REFERENCES tienda_producto (id) ON DELETE CASCADE,
    INDEX tienda_carritoitem_carrito_idx (carrito_id),
    INDEX tienda_carritoitem_producto_idx (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DATOS DE EJEMPLO: Productos iniciales del catálogo
-- =====================================================
INSERT INTO tienda_producto (nombre, color, talla, descripcion, precio, activo, creado, actualizado) VALUES
('Camisa Clásica', 'Rojo', 'M', 'Camisa clásica de algodón premium. Corte recto y botones reforzados.', 29.99, 1, NOW(), NOW()),
('Camisa Slim Fit', 'Negro', 'L', 'Camisa ajustada de vestir. Ideal para ocasiones formales.', 34.99, 1, NOW(), NOW()),
('Camisa Oversize', 'Blanco', 'XL', 'Camisa holgada de estilo urbano. Corte moderno y cómodo.', 24.99, 1, NOW(), NOW());

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
