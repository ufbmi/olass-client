This repo stores the code for the
OneFlorda Linkage Submission System (OLASS) client.


Preliminary rules for creating hashes of patient data:

    # _1 First Name + Last Name + DOB + Zip
    RULE_CODE_F_L_D_Z = 'F_L_D_Z'

    # _2 Last Name + First Name + DOB + Zip
    RULE_CODE_L_F_D_Z = 'L_F_D_Z'

    # _3 First Name + Last Name + DOB + City
    RULE_CODE_F_L_D_C = 'F_L_D_C'

    # _4 Last Name + First Name + DOB + City
    RULE_CODE_L_F_D_C = 'L_F_D_C'

    # _5 Three Letter FN + Three Letter LN + Soundex FN + Soundex LN + DOB
    RULE_CODE_3F_3L_SF_SL_D = '3F_3L_SF_SL_D'
