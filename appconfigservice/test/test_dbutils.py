from appconfig import dbutils

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