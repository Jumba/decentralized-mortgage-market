class Global(object):
    BANKS = {
        'ABN': "3081a7301006072a8648ce3d020106052b8104002703819200040640e99fad5320750b5992e3a9f3ad4457574e393af4c4b90da3ce2a4376ab944f21434cb9032d68bdeb849ed8f7fbe2f6dfae389934b643496c16cbb3b646db0fc366fc89df15de02226d053c803f5b0360f6bd1154556101891fc1c7386b8a11352cc6addde1b6b7beac073512c2003a4825e8ed14cb744ffd2bd437b49d36f23d873c12a5a73e201e2dfd6c2bbeeb",
        'ING': "3081a7301006072a8648ce3d020106052b8104002703819200040077147251457dc6371fe36f1debdd9760d4352d18c0ecd07e76d3119cbc040bc6bed351faba9a4cf92ba95b2155b03bb55de28d4509417241ce278a580c4fbf11746f045759250c04a786270c44e2b66e1d19a5541afaa729f769fcc5ad7e86d0df4ed55fb6c3b1938382b3d6b6b3834776a76e7c25ff1fbe559f7366a79232e2ef380f4fd50485ae9387a84358f8c9",
        'RABO': "3081a7301006072a8648ce3d020106052b81040027038192000406d384d1a81cecea66cb4bfdc10a1097242f90529eafd55fe7470fc22e651d291d93ca64e59c92b417ffc8cfce46f48af579728e0dd7fa3442cf74709adc069907b545fb50477727078a9074a324bfeb81e7224c33b0721a860b64873b41d6bfe7f9d68dcb6532cc5de0b6389d0c89dcb3608444fae0b9e4a3e5b44aef14e296681e4c14181b24d90440c5796ede70fb",
        'MONEYU': "3081a7301006072a8648ce3d020106052b810400270381920004017d26aef2901f36f727958207608bd9e0af16fccde03185f9d0b0d03d6612973cdb7d520b83482d5ab4d471fc4dd24a14056038d2698d8fe1a2e9a623e7c3f6377440def8bcf45d060ac2c1b561852f0e594fed104b4152f8b2ba72b0e0029e1f6b8c74cb257bf3c29146316225d59f887053ea11b2a489844c8d315533adac2d9b2dd323537733e8cd23470d024bcd",
    }

    BANKS_PRIV = {
        'ABN': "3081ee02010104480285c7fba93838cc9ba3abdbd9c501e1190154530d72baf8bbf4e15ecc2c0e83df44db3a4bed85d727ca8b694bf30eb4b146f82f1de8f7d75b26424da98f1c405552c5754787c7c2a00706052b81040027a1819503819200040640e99fad5320750b5992e3a9f3ad4457574e393af4c4b90da3ce2a4376ab944f21434cb9032d68bdeb849ed8f7fbe2f6dfae389934b643496c16cbb3b646db0fc366fc89df15de02226d053c803f5b0360f6bd1154556101891fc1c7386b8a11352cc6addde1b6b7beac073512c2003a4825e8ed14cb744ffd2bd437b49d36f23d873c12a5a73e201e2dfd6c2bbeeb",
        'ING': "3081ee02010104480330de6713c6c4ddd1a933e66992b0d9d496b4dd7238f6dbd4372521ad92a314d6d1f670e279550a6172d8e0bcee46520a23e454ffa580be3da7b062a165f097eefd4649ae43cff5a00706052b81040027a1819503819200040077147251457dc6371fe36f1debdd9760d4352d18c0ecd07e76d3119cbc040bc6bed351faba9a4cf92ba95b2155b03bb55de28d4509417241ce278a580c4fbf11746f045759250c04a786270c44e2b66e1d19a5541afaa729f769fcc5ad7e86d0df4ed55fb6c3b1938382b3d6b6b3834776a76e7c25ff1fbe559f7366a79232e2ef380f4fd50485ae9387a84358f8c9",
        'RABO': "3081ee0201010448027d4af04903e075b9a80cb72ac3f4895b8cc651f6822489b6ed3fbca0d72beb57fc8ccfbe376f79493937862e748a72db2e9c503b3fe848b69e484577827c87452c5cc8b74d1899a00706052b81040027a18195038192000406d384d1a81cecea66cb4bfdc10a1097242f90529eafd55fe7470fc22e651d291d93ca64e59c92b417ffc8cfce46f48af579728e0dd7fa3442cf74709adc069907b545fb50477727078a9074a324bfeb81e7224c33b0721a860b64873b41d6bfe7f9d68dcb6532cc5de0b6389d0c89dcb3608444fae0b9e4a3e5b44aef14e296681e4c14181b24d90440c5796ede70fb",
        'MONEYU': "3081ee020101044802475e22ddb34916fdd32083328a7fdf22b446af0130f7fc2c68d6088751e6eed8cdcdf108ddfdf91f25b6dc56b5b7f6ea7b15f80a942305a3b9f0b5bca80f6f9b3d9a8c33954e2ca00706052b81040027a181950381920004017d26aef2901f36f727958207608bd9e0af16fccde03185f9d0b0d03d6612973cdb7d520b83482d5ab4d471fc4dd24a14056038d2698d8fe1a2e9a623e7c3f6377440def8bcf45d060ac2c1b561852f0e594fed104b4152f8b2ba72b0e0029e1f6b8c74cb257bf3c29146316225d59f887053ea11b2a489844c8d315533adac2d9b2dd323537733e8cd23470d024bcd",
    }


    MASTER_KEY = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                     "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                     "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                     "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")
