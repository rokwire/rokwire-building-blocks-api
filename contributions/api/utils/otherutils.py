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

import uuid

from datetime import datetime

"""
Get current time in UTC format.
"""
def get_current_time_utc():
    currenttime = datetime.utcnow()
    formattedtime, micro = currenttime.strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    formattedtime = "%s.%03dZ" % (formattedtime, int(micro) / 1000)

    return formattedtime

def check_if_uuid(in_uuid):
    is_uuid = False
    try:
        uuid.UUID(in_uuid)
        is_uuid = True
    except Exception:
        is_uuid = False

    return is_uuid

