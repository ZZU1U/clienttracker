from ok_api import OkApi

# TODO MOVE TOKENS TO .ENV

def main():
    ok = OkApi(access_token='-c-2YvM0ZWVR1XE8KcL1eFaGIt4K1v9ICypHJ8zdILi8dJeu5tcDubdf4dcGuRbDTFFuAMYKhrHebXcgPXDQRh4-7tiRQRl5EtQnodHIrm71kDRt4Js0wQi64XHXP6nwRfwvSBbQkgr2pgLoL8sehu0lGNadroJRjvVPBsGv6',
               application_key='CKIKOBLGDIHBABABA',
               application_secret_key='A29086BDC18E6BDBCF2816BE')

    response = ok.friends.get(sort_type='PRESENT')
    for i in response.json():
        pass


if __name__ == '__main__':
    main()