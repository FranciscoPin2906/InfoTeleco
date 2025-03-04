-- Base de datos: `network_devices`
CREATE DATABASE IF NOT EXISTS `network_devices`;
USE `network_devices`;

CREATE TABLE `Company` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `city` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `NetworkDevice` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `device_name` VARCHAR(100) NOT NULL,
  `manufacturer` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  `company_id` INT NOT NULL,
  FOREIGN KEY (`company_id`) REFERENCES `Company` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Router` (
  `id` INT PRIMARY KEY,
  `routing_protocols` VARCHAR(100) NOT NULL,
  `num_ports` INT NOT NULL,
  `firmware_version` VARCHAR(50) NOT NULL,
  `bandwidth` VARCHAR(50) NOT NULL,
  FOREIGN KEY (`id`) REFERENCES `NetworkDevice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Switch` (
  `id` INT PRIMARY KEY,
  `ports` INT NOT NULL,
  `switching_capacity` VARCHAR(50) NOT NULL,
  `mac_address_table_size` INT NOT NULL,
  FOREIGN KEY (`id`) REFERENCES `NetworkDevice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Modem` (
  `id` INT PRIMARY KEY,
  `max_speed` VARCHAR(50) NOT NULL,
  `connection_type` VARCHAR(50) NOT NULL,
  `ipv6_support` BOOLEAN NOT NULL,
  FOREIGN KEY (`id`) REFERENCES `NetworkDevice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `AccessPoint` (
  `id` INT PRIMARY KEY,
  `frequency` VARCHAR(50) NOT NULL,
  `max_clients` INT NOT NULL,
  `security_protocols` VARCHAR(100) NOT NULL,
  `range` VARCHAR(50) NOT NULL,
  FOREIGN KEY (`id`) REFERENCES `NetworkDevice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Route` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `router_id` INT NOT NULL,
  `destination_address` VARCHAR(100) NOT NULL,
  `next_hop` VARCHAR(100) NOT NULL,
  `metric` INT NOT NULL,
  `interface` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`router_id`) REFERENCES `Router` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
