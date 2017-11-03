#DROP TABLE IF EXISTS zone_people;
CREATE TABLE IF NOT EXISTS zone_people (
 id int(11) NOT NULL AUTO_INCREMENT,
 uid varchar(2048) NOT NULL,
 attributes longtext NOT NULL,
 modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS zone_person_zone_service;
CREATE TABLE IF NOT EXISTS zone_person_zone_service (
 zone_person_id int(11) NOT NULL,
 zone_service_id int(11) NOT NULL,
 PRIMARY KEY (zone_person_id,zone_service_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS zone_services;
CREATE TABLE IF NOT EXISTS zone_services (
 id int(11) NOT NULL AUTO_INCREMENT,
 metadata varchar(2048) NOT NULL,
 attributes longtext NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
