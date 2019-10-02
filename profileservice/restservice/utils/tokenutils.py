def get_id_info_from_token(in_token):
    # in_token = convert_str_to_dict(in_token)
    id_type = 0 # 0 for no id string, 1 for pii data, 2 for non-pii
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