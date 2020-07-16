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
