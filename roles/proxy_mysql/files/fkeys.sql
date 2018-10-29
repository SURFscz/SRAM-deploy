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
