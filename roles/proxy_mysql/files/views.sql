DELIMITER $
BEGIN NOT ATOMIC
  IF ( select count(*) from information_schema.views where TABLE_SCHEMA='cotosa' and TABLE_NAME='view_people_services')=1
  THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='view exists';
  ELSE
    create view if not exists view_people_services as
      SELECT
        ps.zone_service_id, s.metadata, s.`attributes` as service_attributes,
        ps.zone_person_id, p.uid, p.`attributes` as person_attributes,p.co_id
        FROM cotosa.zone_person_zone_service as ps
        LEFT JOIN zone_services as s on s.id=ps.zone_service_id
        LEFT JOIN zone_people   as p on p.id=ps.zone_person_id
        ;
  END IF;
END $
DELIMITER ;
