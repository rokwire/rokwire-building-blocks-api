def get_id_info_from_token(in_token):
    # in_token = convert_str_to_dict(in_token)
    id_type = 0 # 0 for no pii, 1 for uin id, 2 phone id
    id_string = ""

    # check if the pii token is from campus or from outside the campus
    # if there is uin, it is from campus
    if 'uiucedu_uin' in in_token:
        id_string = in_token['uiucedu_uin']
        id_type = 1

    # if there is phone number, it is from outside the campus
    if 'phoneNumber' in in_token:
        id_string = in_token['phoneNumber']
        id_type = 2

    return id_type, id_string


def convert_str_to_dict(in_token):
    while True:
        try:
            converted_dict = eval(in_token)
        except NameError as e:
            key = e.message.split("'")[1]
            in_token = in_token.replace(key, "'{}'".format(key))
        else:
            return converted_dict

def get_data_from_token(in_token):
    tk_is_uin = False
    tk_is_phone = False
    tk_uin = None
    tk_firstname = None
    tk_lastname = None
    tk_email = None
    tk_phone = None

    try:
        tk_uin = in_token['uiucedu_uin']
        tk_is_uin = True
    except:
        pass
    try:
        tk_firstname = in_token['given_name']
    except:
        pass
    try:
        tk_lastname = in_token['family_name']
    except:
        pass
    try:
        tk_email = in_token['email']
    except:
        pass
    try:
        tk_phone = in_token['phoneNumber']
        tk_is_phone = True
    except:
        pass

    return tk_uin, tk_firstname, tk_lastname, tk_email, tk_phone, tk_is_uin, tk_is_phone