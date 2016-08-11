# Intro

The data elements of a patient can be combined in different ways and then
hashed using sha256 algorithm in order to produce unique identifiers.
Two patients will obtain the same UUID from the
[olass-server](https://github.com/ufbmi/olass-server) application if hashes of
their data elements match.

Preliminary rules for creating hashes of patient data:

    # _1 First Name + Last Name + DOB + Zip
    RULE_CODE_F_L_D_Z = 'F_L_D_Z'

    # _2 Last Name + First Name + DOB + Zip
    RULE_CODE_L_F_D_Z = 'L_F_D_Z'

    # _3 First Name + Last Name + DOB + City
    RULE_CODE_F_L_D_C = 'F_L_D_C'

    # _4 Last Name + First Name + DOB + City
    RULE_CODE_L_F_D_C = 'L_F_D_C'


