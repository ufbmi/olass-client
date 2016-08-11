
DROP DATABASE IF EXISTS olassc;

REVOKE ALL PRIVILEGES ON olassc.* FROM 'olassc'@'localhost';
DROP USER 'olassc'@'localhost';
FLUSH PRIVILEGES;
