#  Copyright 2020 Board of Trustees of the University of Illinois.
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

def get_id_info_from_token(in_token):
    # in_token = convert_str_to_dict(in_token)
    id_type = 0 # 0 for no pii, 1 for uin id, 2 phone id
    id_string = ""


    # check if the pii token is from campus or from outside the campus
    # if there is uin, it is from campus
    if 'uiucedu_uin' in in_token:
        id_string = in_token['uiucedu_uin']
        id_type = 1

    # TODO following lines are modified to use email instead of uin in id checking
    #  for GET, POST, and DELETE
    # # if there is email, it is from campus
    # if 'email' in in_token:
    #     id_string = in_token['email']
    #     id_type = 1

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
    tk_uin = in_token.get('uiucedu_uin')
    tk_is_uin = tk_uin is not None
    tk_firstname = in_token.get('given_name')
    tk_lastname = in_token.get('family_name')
    tk_email = in_token.get('email')
    tk_phone = in_token.get('phoneNumber')
    tk_is_phone = tk_phone is not None

    return tk_uin, tk_firstname, tk_lastname, tk_email, tk_phone, tk_is_uin, tk_is_phone