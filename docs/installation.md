# Installation pre-requisites

Each installation of the OLASS client will need access to a local database
with patient information. University of Florida will provide additional
configuration parameters required for sending hashed data to the OLASS server
component deployed at UF's data center.

Below is the list of required parameters:

- access credentials and the ip address for the MySQL or MSSQL database server
        `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`
- access credentials for the server
        `CLIENT_ID`, `CLIENT_SECRET`
- the OLASS server endpoint addresses:
        `TOKEN_URL`, `SAVE_URL`
- data parsing parameters:
        `SALT`, `ENABLED_RULES`


# RedHat Linux

For installation instructions specific to RedHat Linux please
follow the steps from [installation-redhat.md](installation-redhat.md)


# Windows

For installation instructions specific to Windows please
follow the steps from [installation-windows.md](installation-windows.md)


# Help with installation

If you encounter any issuse or have suggestions for improving the installation
instructions please send us an email at <pre>bmi-developers [*at*] ad.ufl.edu </pre>

We appreciate your feedback.
