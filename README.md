# OLASS Client

| Branch | [Travis-CI](https://travis-ci.org/ufbmi/olass-client/builds) | [Coveralls](https://coveralls.io/github/ufbmi/olass-client) |
| :----- | :---------------------------: | :-------: |
| [Master](https://github.com/ufbmi/olass-client/tree/master) | [![Master](https://travis-ci.org/ufbmi/olass-client.svg?branch=master)](https://travis-ci.org/ufbmi/olass-client) | [![Coverage Status](https://coveralls.io/repos/github/indera/olass-client/badge.svg?branch=master)](https://coveralls.io/github/indera/olass-client?branch=master)
| [Develop](https://github.com/ufbmi/olass-client/tree/develop) | [![Develop](https://travis-ci.org/ufbmi/olass-client.svg?branch=develop)](https://travis-ci.org/ufbmi/olass-client) | [Master](https://github.com/ufbmi/olass-client/tree/master) | [![Master](https://travis-ci.org/ufbmi/olass-client.svg?branch=master)](https://travis-ci.org/ufbmi/olass-client) | [![Coverage Status](https://coveralls.io/repos/github/indera/olass-client/badge.svg?branch=develop)](https://coveralls.io/github/indera/olass-client?branch=develop)

# Introduction

This repo stores the code for the OneFlorda Linkage Submission System (OLASS)
client application.

The goal of the OLASS client is to compute hashes of the patient data elements
and submit them to the OLASS server to achieve de-duplication.
The client obtains an access token from the server, submits json data
to the `/api/save` endpoint, and receives back an unique identifier (UUID)
for each patient.


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

## Contributors

The application was designed and implemented by Andrei Sura with tremendous
support, fedback and contributions from the
[BMI team](https://github.com/orgs/ufbmi/people).

For the complete list of contributors please see [AUTHORS.md](AUTHORS.md)
