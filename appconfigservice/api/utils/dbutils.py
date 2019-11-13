import re

APP_VERION_REGX = "^\d+.\d+.\d+$"
VERSION_NUMBER_REGX = '^(\d+).(\d+).(\d+)$'


def check_appversion_format(version):
    m = re.match(APP_VERION_REGX, version)
    matched = False
    if m:
        matched = (m.group(0) == version)
    return matched


def create_version_numbers(version):
    version_numbers = {}
    m = re.match(VERSION_NUMBER_REGX, version)
    if m:
        version_numbers['major'] = int(m.group(1))
        version_numbers['minor'] = int(m.group(2))
        version_numbers['patch'] = int(m.group(3))
    return version_numbers
