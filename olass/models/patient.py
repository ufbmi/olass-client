"""
Goal: Implement ORM for `patient` table
"""
import sqlalchemy as db
from olass.models.base import DeclarativeBase
from olass.models.crud_mixin import CRUDMixin

__all__ = ['Patient']

"""
+---------------------+---------------------+------+-----+---------+
| Field               | Type                | Null | Key | Default |
+---------------------+---------------------+------+-----+---------+
| pat_id              | bigint(20) unsigned | NO   | PRI | NULL    |
| pat_mrn             | varchar(255)        | NO   | UNI | NULL    |
| linkage_uuid        | binary(16)          | YES  | MUL | NULL    |
| linkage_added_at    | datetime            | YES  | MUL | NULL    |
| gender              | char(2)             | YES  | MUL | NULL    |
| race                | char(2)             | YES  | MUL | NULL    |
| hispanic_ethnicity  | char(2)             | YES  | MUL | NULL    |
| pat_birth_date      | date                | NO   |     | NULL    |
| pat_first_name      | varchar(255)        | NO   |     | NULL    |
| pat_last_name       | varchar(255)        | NO   |     | NULL    |
| pat_middle_name     | varchar(255)        | YES  |     | NULL    |
| pat_phone           | varchar(255)        | YES  |     | NULL    |
| pat_address_line1   | varchar(255)        | YES  |     | NULL    |
| pat_address_line2   | varchar(255)        | YES  |     | NULL    |
| pat_address_city    | varchar(255)        | YES  |     | NULL    |
| pat_address_state   | char(2)             | YES  |     | NULL    |
| pat_address_zip     | char(10)            | YES  |     | NULL    |
| pat_address_country | char(2)             | YES  |     | NULL    |
+---------------------+---------------------+------+-----+---------+
"""


class Patient(CRUDMixin, DeclarativeBase):
    """
    Store data about the patient
    """
    __tablename__ = 'patient'
    id = db.Column('pat_id', db.Integer, primary_key=True)
    pat_mrn = db.Column('pat_mrn', db.Text, nullable=False)

    # These two columns are populated when we receive json from OLASS server
    linkage_uuid = db.Column('linkage_uuid', db.Binary)
    linkage_added_at = db.Column('linkage_added_at', db.DateTime)

    # used columns
    pat_gender = db.Column('gender', db.Text)
    pat_birth_date = db.Column('pat_birth_date', db.DateTime, nullable=False)
    pat_first_name = db.Column('pat_first_name', db.Text, nullable=False)
    pat_last_name = db.Column('pat_last_name', db.Text, nullable=False)

    pat_address_city = db.Column('pat_address_city', db.Text)
    pat_address_zip = db.Column('pat_address_zip', db.Text)

    # Optional columns
    pat_middle_name = db.Column('pat_middle_name', db.Text)
    pat_address_line1 = db.Column('pat_address_line1', db.Text)
    pat_address_line2 = db.Column('pat_address_line2', db.Text)
