# OLASS Client

| Branch | [Travis-CI](https://travis-ci.org/ufbmi/olass-client/builds) | [Coveralls](https://coveralls.io/github/ufbmi/olass-client) |
| :----- | :---------------------------: | :-------: |
| [Master](https://github.com/ufbmi/olass-client/tree/master) | [![Master](https://travis-ci.org/ufbmi/olass-client.svg?branch=master)](https://travis-ci.org/ufbmi/olass-client) | [![Coverage Status](https://coveralls.io/repos/github/ufbmi/olass-client/badge.svg?branch=master)](https://coveralls.io/github/ufbmi/olass-client?branch=master)
| [Develop](https://github.com/ufbmi/olass-client/tree/develop) | [![Develop](https://travis-ci.org/ufbmi/olass-client.svg?branch=develop)](https://travis-ci.org/ufbmi/olass-client) | [![Coverage Status](https://coveralls.io/repos/github/ufbmi/olass-client/badge.svg?branch=develop)](https://coveralls.io/github/ufbmi/olass-client?branch=develop)


OneFlorda Linkage Submission System (OLASS) client software
<https://github.com/ufbmi/olass-client> is designed to compute hashes of the
specific patient data elements and submit them to the OLASS server
<https://github.com/ufbmi/olass-server> to achieve de-duplication.

The client authorizes using the OAuth2 protocol on the server, submits the
hashes, and receives back an uniqueidentifier (UUID) for each patient.
The UUID is used later for submission of medical records such as
demographics, procedures, diagnoses, vitals, lab results.


# Authentication

The client is implemented using the 
[python oauthlib](http://oauthlib.readthedocs.io/en/latest/oauth2/clients/backendapplicationclient.html)
library and it follows the "client credentials" grant workflow described in the
[rfc6749](https://tools.ietf.org/html/rfc6749#section-1.3.4).


    +---------+                                  +---------------+
    :         :                                  :               :
    :         :>-- A - Client Authentication --->: Authorization :
    : Client  :                                  :     Server    :
    :         :<-- B ---- Access Token ---------<:               :
    :         :                                  :               :
    +---------+                                  +---------------+


# License

This project is covered by the [MIT License](LICENSE).


# Installation

The client application depends on proper configuration in order to interact
with the [olass-server](https://github.com/ufbmi/olass-server).
For more details please refer to the
[docs/installation.md](docs/installation.md)


# Contributors

The application was designed and implemented by Andrei Sura with tremendous
support, fedback and contributions from the
[BMI team](https://github.com/orgs/ufbmi/people).

For the complete list of contributors please see [AUTHORS.md](AUTHORS.md)
