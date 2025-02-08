-- Structure de la table customers
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `balance` float DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table customers
INSERT INTO customers VALUES ('1', 'SidM'hamed Avdhil', '46423332', 'sidmhamedavdhil@gmail.com', 'لدوحة كرفور المخطار فراج الدوحة', '2024-12-04 20:26:59', '200.0', '0');
INSERT INTO customers VALUES ('5', ' عبد الرزاق ببان', '22312121', 'abdou@gmail.com', 'النعمة', '2025-01-17 18:13:19', '123.0', '0');
INSERT INTO customers VALUES ('6', 'محمد ببانه', '32323232', 'babana@gmail.com', 'عرفات', '2025-01-17 18:41:38', '43.0', '1');
INSERT INTO customers VALUES ('12', 'mouhamed', '12212112', 'dah@gmail.com', 'arafat', '2025-02-05 20:14:13', '12.0', '0');

-- Structure de la table licenses
CREATE TABLE `licenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac_address` varchar(17) NOT NULL,
  `license_key` varchar(64) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac_address` (`mac_address`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Structure de la table mac
CREATE TABLE `mac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mac_address` varchar(17) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac_address` (`mac_address`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Données de la table mac
INSERT INTO mac VALUES ('6', '84-7B-EB-3C-49-74', '2025-02-07 18:48:19');

-- Structure de la table product_categories
CREATE TABLE `product_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table product_categories
INSERT INTO product_categories VALUES ('1', 'Car Parts ', 'Electronic components and accessories bb fdsfdsfsdfdfdfdsfdfdfdsfffd', '2025-01-27 21:19:41');
INSERT INTO product_categories VALUES ('2', 'Electronics', 'Electronic components and accessories aa', '2024-12-07 00:00:00');
INSERT INTO product_categories VALUES ('3', 'Mechanical', 'Mechanical parts and components', '2025-01-15 00:00:00');

-- Structure de la table product_units
CREATE TABLE `product_units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `symbol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure de la table products
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `price` float NOT NULL,
  `purchase_price` float DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `selling_price` float DEFAULT NULL,
  `quantity` float DEFAULT NULL,
  `min_quantity` float DEFAULT '0',
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `code_2` (`code`),
  KEY `supplier_id` (`supplier_id`),
  KEY `warehouse_id` (`warehouse_id`),
  KEY `unit_id` (`unit_id`),
  KEY `fk_product_category` (`category_id`),
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`),
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouses` (`id`),
  CONSTRAINT `products_ibfk_4` FOREIGN KEY (`unit_id`) REFERENCES `product_units` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table products
INSERT INTO products VALUES ('3', 'Car Part 1', 'High-quality car part number 1, compatible with various car models.', '800.0', '600.0', '1', '1', '2024-12-06 00:00:00', '1', 'PROD3', NULL, '1000.0', '261.0', '180.0', '1');
INSERT INTO products VALUES ('4', 'Car Part 2', 'High-quality car part number 2, compatible with various car models.', '260.0', '200.0', '3', '1', '2024-12-04 00:00:00', '3', 'PROD4', NULL, '300.0', '52.0', '100.0', '1');

-- Structure de la table sale_items
CREATE TABLE `sale_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sale_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` float NOT NULL,
  `discount` float DEFAULT NULL,
  `subtotal` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `sale_items_ibfk_2` (`sale_id`),
  CONSTRAINT `sale_items_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `sale_items_ibfk_2` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table sale_items
INSERT INTO sale_items VALUES ('31', '30', '3', '3.0', NULL, '3000.0');
INSERT INTO sale_items VALUES ('32', '30', '4', '1.0', NULL, '300.0');
INSERT INTO sale_items VALUES ('33', '31', '3', '2.0', NULL, '2000.0');
INSERT INTO sale_items VALUES ('34', '32', '3', '1.0', NULL, '1000.0');
INSERT INTO sale_items VALUES ('35', '34', '4', '2.0', NULL, '600.0');
INSERT INTO sale_items VALUES ('36', '35', '3', '3.0', NULL, '3000.0');
INSERT INTO sale_items VALUES ('37', '35', '4', '1.0', NULL, '300.0');
INSERT INTO sale_items VALUES ('38', '36', '3', '3.0', NULL, '3000.0');
INSERT INTO sale_items VALUES ('39', '37', '3', '4.0', NULL, '4000.0');
INSERT INTO sale_items VALUES ('40', '37', '4', '1.0', NULL, '300.0');
INSERT INTO sale_items VALUES ('41', '38', '3', '1.0', NULL, '1000.0');
INSERT INTO sale_items VALUES ('42', '39', '4', '1.0', NULL, '300.0');
INSERT INTO sale_items VALUES ('44', '39', '3', '1.0', NULL, '1000.0');

-- Structure de la table sales
CREATE TABLE `sales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment_method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_by` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference_number` (`reference_number`),
  KEY `created_by` (`created_by`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table sales
INSERT INTO sales VALUES ('30', '2025-01-26 00:00:00', '1', 'gdfgf', 'card', 'Azerty12', 'fdgfdgfdgfdg', '1', '2025-01-26 00:13:42', '2025-01-26 00:13:42');
INSERT INTO sales VALUES ('31', '2025-01-26 00:00:00', '1', 'fsdfds', 'card', '123SSS', 'DSFDSFDFS', '1', '2025-01-26 00:30:42', '2025-01-26 00:30:42');
INSERT INTO sales VALUES ('32', '2025-01-26 00:00:00', '1', 'good', 'cash', 'C5967258', 'note', '1', '2025-01-26 21:31:20', '2025-01-26 21:31:20');
INSERT INTO sales VALUES ('34', '2025-01-27 00:00:00', '5', 'ok', 'sfdfsd', '4F9C4348', 'fdsff', '1', '2025-01-27 16:14:09', '2025-01-27 16:14:09');
INSERT INTO sales VALUES ('35', '2025-01-27 17:52:03', '1', 'dfsdf', 'dgdgf', '57922268', 'gdfdfg', '1', '2025-01-27 17:51:30', '2025-01-27 17:35:30');
INSERT INTO sales VALUES ('36', '2025-02-02 00:00:00', '1', 'dsf', 'card', 'B72E3583', 'fdsfsdfsf', '1', '2025-02-02 23:36:06', '2025-02-02 23:36:06');
INSERT INTO sales VALUES ('37', '2025-02-03 00:00:00', '1', 'ok', 'money', 'C0A59247', 'nice', '1', '2025-02-03 16:36:39', '2025-02-03 16:36:39');
INSERT INTO sales VALUES ('38', '2025-02-04 00:00:00', '1', 'dfdfsf', 'dfsf', '52F85166', 'fgfdgdf', '1', '2025-02-04 16:48:04', '2025-02-04 16:48:04');
INSERT INTO sales VALUES ('39', '2025-02-04 00:00:00', '1', 'ready', 'card', 'F6C96744', 'ok', '1', '2025-02-04 20:00:28', '2025-02-04 20:00:28');

-- Structure de la table suppliers
CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `credit_limit` float DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `email_2` (`email`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table suppliers
INSERT INTO suppliers VALUES ('1', 'Ahmed', '31310090', 'ahmed@gmail.com', 'ndb', '2024-12-04 14:30:00', '2024-12-04 14:30:00', '0.0', '3');
INSERT INTO suppliers VALUES ('3', 'محمد', '22121212', 'mouhamed@gmail.com', 'النعمة', '2025-01-16 20:22:52', '2025-01-16 20:22:52', '55.0', '1');
INSERT INTO suppliers VALUES ('4', 'rady', '54545455', 'rady@gmail.com', 'ndb', '2025-01-16 20:23:28', '2025-01-16 20:23:28', '1234.0', '1');
INSERT INTO suppliers VALUES ('5', 'Sidy', '32423434', 'sidi@gmail.com', 'atar', '2025-01-16 21:04:00', '2025-01-16 21:04:00', '0.0', '1');
INSERT INTO suppliers VALUES ('6', 'moulay', '3232323', 'moulay@gmail.com', 'riyad', '2025-01-16 21:30:21', '2025-01-16 21:30:21', '0.0', '1');
INSERT INTO suppliers VALUES ('8', 'Abdy', '23232233', 'abdy@gmial.com', 'Arafat', '2025-01-18 16:37:20', '2025-01-18 16:37:20', '12.0', '1');
INSERT INTO suppliers VALUES ('13', 'dady', '23232323', 'dady@isce.mr', 'nema', '2025-02-04 18:47:25', '2025-02-04 18:47:25', NULL, NULL);
INSERT INTO suppliers VALUES ('16', 'dalla', '22121213', 'dalla@gmail.com', 'Atar', '2025-02-04 18:58:27', '2025-02-04 18:58:27', NULL, NULL);

-- Structure de la table system_settings
CREATE TABLE `system_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `options` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_public` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table system_settings
INSERT INTO system_settings VALUES ('1', 'company_name', 'شركتي', 'اسم الشركة الذي سيظهر في الفواتير والتقارير', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'اسم الشركة', 'text', NULL, 'company', '1');
INSERT INTO system_settings VALUES ('2', 'company_address', '', 'عنوان الشركة الذي سيظهر في الفواتير', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'عنوان الشركة', 'textarea', NULL, 'company', '1');
INSERT INTO system_settings VALUES ('3', 'company_phone', '', 'رقم هاتف الشركة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'هاتف الشركة', 'text', NULL, 'company', '1');
INSERT INTO system_settings VALUES ('4', 'company_email', '', 'البريد الإلكتروني للشركة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'البريد الإلكتروني للشركة', 'text', NULL, 'company', '1');
INSERT INTO system_settings VALUES ('5', 'company_tax_number', '', 'الرقم الضريبي للشركة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'الرقم الضريبي', 'text', NULL, 'company', '1');
INSERT INTO system_settings VALUES ('6', 'invoice_font_size', '14', 'حجم الخط المستخدم في طباعة الفاتورة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'حجم خط الفاتورة', 'number', NULL, 'print', '1');
INSERT INTO system_settings VALUES ('7', 'invoice_paper_size', 'A4', 'حجم الورق المستخدم في طباعة الفاتورة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'حجم ورق الفاتورة', 'select', 'A4,A5,Letter', 'print', '1');
INSERT INTO system_settings VALUES ('8', 'invoice_header_image', '', 'الشعار الذي سيظهر في أعلى الفاتورة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'شعار الفاتورة', 'file', NULL, 'print', '1');
INSERT INTO system_settings VALUES ('9', 'invoice_footer_text', 'شكراً لتعاملكم معنا', 'النص الذي سيظهر في أسفل الفاتورة', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'نص تذييل الفاتورة', 'textarea', NULL, 'print', '1');
INSERT INTO system_settings VALUES ('10', 'print_extra_copies', '1', 'عدد النسخ الإضافية التي سيتم طباعتها تلقائياً', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'عدد النسخ الإضافية', 'number', NULL, 'print', '1');
INSERT INTO system_settings VALUES ('11', 'currency', 'الأوقية', 'رمز العملة المستخدمة', '2024-12-05 09:42:26', '2024-12-05 19:45:15', 'العملة', 'string', '', 'company', '1');
INSERT INTO system_settings VALUES ('12', 'language', 'ar', 'لغة النظام', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'اللغة', 'select', 'ar,en,fr', 'general', '1');
INSERT INTO system_settings VALUES ('13', 'timezone', 'Africa/Algiers', 'المنطقة الزمنية للنظام', '2024-12-05 09:42:26', '2024-12-05 09:42:26', 'المنطقة الزمنية', 'text', NULL, 'general', '1');

-- Structure de la table users
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table users
INSERT INTO users VALUES ('1', 'admin', 'admin@example.com', '$2b$12$dm4fKuEEc8uOLUPgCyJY4O8vg7xDm2uROMhYBLVB9lozY9ErnaU4C', '1', '2024-12-04 12:38:11', '2025-01-19 21:01:24');
INSERT INTO users VALUES ('4', 'ahmed', 'ahmed@gmail.com', '$2b$12$5VDxZ1Xvvc3wA4YNfoZ/V.GgnNBlDVW1NaZK7An4dj/ZephkTzDmq', '0', '2025-01-18 21:55:26', '2025-01-18 21:55:26');
INSERT INTO users VALUES ('6', 'Aly1', 'aly@gmail.com', '$2b$12$plaVQfMphMCQrzeGdbtmdu8FLQDF2dn5AGr5PNZHSX0Y/Q8Rv/Z1u', '0', '2025-02-05 20:21:37', '2025-02-07 15:38:16');

-- Structure de la table warehouses
CREATE TABLE `warehouses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Données de la table warehouses
INSERT INTO warehouses VALUES ('1', 'stock 1', 'Center Emteur', 'Stock One in center emeteur', '1', '2024-12-04 18:14:01', '2024-12-04 18:14:01', '100');
INSERT INTO warehouses VALUES ('2', 'Warehouse 1', 'NKTT-N', 'تم إنشاؤه تلقائياً عند استيراد المنتجات', '1', '2024-12-04 22:30:31', '2024-12-05 11:44:05', '1050');
INSERT INTO warehouses VALUES ('3', 'Warehouse 2', 'NKTT-T', 'تم إنشاؤه تلقائياً عند استيراد المنتجات', '1', '2024-12-04 22:30:31', '2024-12-04 22:30:31', '900');
INSERT INTO warehouses VALUES ('4', 'Warehouse 3', 'NKTT-West', 'تم إنشاؤه تلقائياً عند استيراد المنتجات', '1', '2024-12-04 22:30:31', '2025-01-28 17:29:02', '900');
INSERT INTO warehouses VALUES ('5', 'Warehouse 44', 'NKTT-E', 'تم إنشاؤه تلقائياً عند استيراد المنتجات', '1', '2024-12-04 22:30:31', '2025-02-02 21:17:34', '1100');
INSERT INTO warehouses VALUES ('6', 'Warehouse 0', 'NKTT-S', 'تم إنشاؤه تلقائياً عند استيراد المنتجات', '1', '2024-12-04 22:30:31', '2024-12-05 11:41:52', '1200');
INSERT INTO warehouses VALUES ('15', 'ggg', 'dg', 'fdsf', NULL, NULL, '2025-02-05 20:16:51', NULL);

