

def decodeit(id_token):
    import jwt
    import credentials
    return {
        'id_token': jwt.decode(
            id_token,
            credentials.PHONE_VERIFY_SECRET,
            audience=credentials.PHONE_VERIFY_AUDIENCE,
        ),
        'unver_header': jwt.get_unverified_header(id_token),
    }
