
-- Store database modification log
CREATE TABLE version (
     version_id varchar(255) NOT NULL DEFAULT '',
    version_stamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    version_info text NOT NULL,
  PRIMARY KEY (version_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO version (version_id, version_stamp, version_info)
   VALUES('001', now(), 'New tables: version, gender, race, hispanic_ethnicity, patient')
;

CREATE TABLE gender (
    gender char(2) NOT NULL,
    gender_name varchar(255) NOT NULL,
    gender_description TEXT,
 PRIMARY KEY (gender)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE race (
    race char(2) NOT NULL,
    race_name varchar(255) NOT NULL,
    race_description TEXT,
 PRIMARY KEY (race)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE hispanic_ethnicity (
    hispanic_ethnicity char(2) NOT NULL,
    hispanic_ethnicity_name varchar(255) NOT NULL,
    hispanic_ethnicity_description TEXT,
 PRIMARY KEY (hispanic_ethnicity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- When the partner populates the initial patient data
-- the `linkage_uuid`, and `linkage_added_at` columns are null
-- TODO: check if `pat_mrn` column should be unique key
CREATE TABLE patient (
    pat_id bigint unsigned NOT NULL AUTO_INCREMENT,
    pat_mrn varchar(255) NOT NULL,
    linkage_uuid binary(16),
    linkage_added_at datetime,
    gender char(2),
    race char(2),
    hispanic_ethnicity char(2),
    pat_birth_date date             NOT NULL,
    pat_first_name varchar(255)     NOT NULL,
    pat_last_name varchar(255)      NOT NULL,
    pat_middle_name varchar(255),
    pat_phone varchar(255),
    pat_address_line1 varchar(255),
    pat_address_line2 varchar(255),
    pat_address_city varchar(255),
    pat_address_state char(2),
    pat_address_zip char(10),
    pat_address_country CHAR(2),
 PRIMARY KEY (pat_id),
 KEY (pat_mrn),
 KEY (linkage_uuid),
 KEY (linkage_added_at),
 KEY (gender),
 KEY (race),
 KEY (hispanic_ethnicity),
 CONSTRAINT `fk_patient_gender` FOREIGN KEY (gender) REFERENCES gender (gender),
 CONSTRAINT `fk_patient_race` FOREIGN KEY (race) REFERENCES race (race),
 CONSTRAINT `fk_patient_hispanic_ethnicity` FOREIGN KEY (hispanic_ethnicity) REFERENCES hispanic_ethnicity (hispanic_ethnicity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
