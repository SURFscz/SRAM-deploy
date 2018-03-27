CREATE TABLE `attributes_hash` (
  `nameid` varchar(50) NOT NULL,
  `hash` varchar(45) DEFAULT NULL,
  UNIQUE KEY `nameid` (`nameid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
