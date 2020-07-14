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

from ..utils import dbutils


def test_valid_appversion():
    vers_1 = "0.1.0"
    is_valid = dbutils.check_appversion_format(vers_1)
    assert is_valid == True
    vers_2 = "12.0.10"
    is_valid = dbutils.check_appversion_format(vers_2)
    assert is_valid == True


def test_invalid_appversion():
    vers_1 = "0.1.2.3.4"
    is_valid = dbutils.check_appversion_format(vers_1)
    assert is_valid == False
    vers_2 = "a.b.c"
    is_valid = dbutils.check_appversion_format(vers_2)
    assert is_valid == False
