
CREATE DATABASE olass;

-- Create the user and grant privileges
CREATE USER 'olass'@'localhost' IDENTIFIED BY 'insecurepassword';

FLUSH PRIVILEGES;

GRANT
    ALL PRIVILEGES
ON
    olass.*
TO
    'olass'@'localhost';
