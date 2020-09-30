from datetime import date


def init_talent():
    d = {
        "name": '',
        "shortDescription": '',
        "longDescription": '',
        "requiredCapabilities": [],
        "requiredBuildingBlocks": [],
        "minUserPrivacyLevel": 1,
        "minEndUserRoles": [],
        "startDate": date.today().strftime("%d/%m/%Y"),
        "endDate": date.today().strftime("%d/%m/%Y"),
        "dataDescription": '',
        "selfCertification": {
            "dataDeletionUponRequest": '',
            "respectingUserPrivacySetting": '',
            "discloseAds": '',
            "discloseSponsors": '',
            "discloseImageRights": ''
        }
    }
    return d


def to_talent(d):
    if not d: return {}
    talent_list = []

    if isinstance(d['talent_name'], str):
        talent_list.append(init_talent())
    else:
        for _ in range(len(d['talent_name'])):
            talent_list.append(init_talent())

    for i, talent in enumerate(talent_list):
        for k, v in d.items():
            print(k, v)

            if "minUserPrivacyLevel" in k:
                if len(v[i]) > 0:
                    talent_list[i]["minUserPrivacyLevel"] = int(v[i])
                d[k][i] = talent_list[i]["minUserPrivacyLevel"]
            if "talent_" in k:
                name = k.split("talent_")[-1]
                if name in talent_list[i] and isinstance(talent_list[i][name], list) and len(v[i]) > 0:
                    talent_list[i][name].append(v[i])
                elif name in talent_list[i] and isinstance(talent_list[i][name], list) and len(v[i]) == 0:
                    talent_list[i][name] = []
                else:
                    talent_list[i][name] = v[i]
    return talent_list
