import re

APP_VERION_REGX = "^\d+.\d+.\d+$"

def check_appversion_format(version):
    m = re.match(APP_VERION_REGX, version)
    matched = False
    if m:
        matched = (m.group(0) == version)
    return matched