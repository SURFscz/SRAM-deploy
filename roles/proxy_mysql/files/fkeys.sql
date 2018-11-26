DELIMITER $
BEGIN NOT ATOMIC
  IF ( select count(*) from information_schema.key_column_usage where CONSTRAINT_NAME='fk_zone_person_id' AND TABLE_SCHEMA='cotosa' and TABLE_NAME='zone_person_zone_service')=1
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='key exists';
  ELSE
    ALTER TABLE zone_person_zone_service
      ADD CONSTRAINT fk_zone_person_id FOREIGN KEY IF NOT EXISTS
      (zone_person_id) REFERENCES zone_people (id)
      ON DELETE cascade
      ON UPDATE restrict;

    ALTER TABLE zone_person_zone_service
      ADD CONSTRAINT fk_zone_service_id FOREIGN KEY IF NOT EXISTS
      (zone_service_id) REFERENCES zone_services (id)
      ON DELETE cascade
      ON UPDATE restrict;

  END IF;
END $
DELIMITER ;
