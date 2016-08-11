
INSERT INTO gender
    (gender, gender_name, gender_description)
VALUES
    ('A', 'Ambiguous', 'May be used for individuals who are physically undifferentiaded from birth'),
    ('F',  'Female', ''),
    ('M',  'Male', ''),
    ('NI', 'No information', ''),
    ('UN', 'Unknown', ''),
    ('OT', 'Other', 'May ne used for individuals who are undergoing gender re-assignment')
;


INSERT INTO race
    (race, race_name, race_description)
VALUES
    ('01', 'American Indian or Alaska Native',
        'A person having origins in any of the original peoples of North and South America (including Central America), and who maintains tribal affiliation or community attachment'),
    ('02', 'Asian',
        'A person having origins in any of the original peoples of the Far East, Southeast Asia, or the Indian subcontinent including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand, and Vietnam.'),
    ('03', 'Black or African American',
        'A person having origins in any of the black racial groups of Africa.'),
    ('04', 'Native Hawaiian or Other Pacific Islander',
        'A person having origins in any of the original peoples of Hawaii, Guam, Samoa, or other Pacific Islands.'),
    ('05', 'White',
        'A person having origins in any of the original peoples of Europe, the Middle East, or North Africa.'),
    ('06', 'Multiple race', ''),
    ('07', 'Refuse to answer', ''),
    ('NI', 'No information', ''),
    ('UN', 'Unknown', ''),
    ('OT', 'Other', '')
;


INSERT INTO hispanic_ethnicity
    (hispanic_ethnicity, hispanic_ethnicity_name, hispanic_ethnicity_description)
VALUES
    ('Y', 'Yes', 'A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin, regardless of race'),
    ('N', 'No', ''),
    ('R', 'Refuse to answer', ''),
    ('NI', 'No information', ''),
    ('UN', 'Unknown', ''),
    ('OT', 'Other', '')
;

INSERT INTO patient
    (pat_mrn, pat_birth_date, pat_first_name, pat_last_name, pat_address_city, pat_address_zip)
VALUES
    ('mrn_001', '1950-01-01', 'Abc', 'Def', 'Gainesville', '32606')
;

SHOW TABLES;
/*
SELECT * FROM version;
SELECT * FROM gender;
SELECT * FROM race;
SELECT * FROM hispanic_ethnicity_description;
*/
SELECT pat_mrn, pat_birth_date, pat_first_name, pat_last_name, pat_address_city, pat_address_zip FROM patient;
