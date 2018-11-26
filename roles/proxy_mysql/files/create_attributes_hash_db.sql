DELIMITER $
BEGIN NOT ATOMIC
  IF ( select count(*) from information_schema.tables where TABLE_SCHEMA='attributes_hash' and TABLE_NAME='zone_people')=1
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='table exists';
  ELSE
    CREATE TABLE `attributes_hash` (
    `nameid` varchar(50) NOT NULL,
    `hash` varchar(45) DEFAULT NULL,
    UNIQUE KEY `nameid` (`nameid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  END IF;
END $
DELIMITER ;
