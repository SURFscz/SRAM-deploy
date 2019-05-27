DELIMITER $
BEGIN NOT ATOMIC
  IF ( select count(*) from information_schema.columns where TABLE_SCHEMA='cotosa' and TABLE_NAME='zone_people' and COLUMN_NAME='co_person_id')=1
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='column exists';
  ELSE
    DELETE from zone_people;
    DELETE from zone_services;
    ALTER TABLE zone_people ADD COLUMN co_person_id INT not null;
    ALTER TABLE zone_people ADD COLUMN modified TIMESTAMP;
    ALTER TABLE zone_services ADD COLUMN co_service_id INT not null;
  END IF;
END $
DELIMITER ;
