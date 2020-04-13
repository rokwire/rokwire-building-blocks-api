import copy

from models.interest import Interest
from models.favorites import Favorites
from models.privacysettings import PrivacySettings

"""
set non pii dataset
"""
def update_non_pii_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_file_descriptors(injson['fileDescriptors'])
        del outjson['fileDescriptors']
    except:
        pass
    try:
        dataset.set_over13(injson['ifOpenSource'])
        del outjson['ifOpenSource']
    except:
        pass
    try:
        # check if it is a first description
        if dataset.get_interests() is not None:
            for i in range(len(injson["description"])):
                interest = Interest()
                category = injson["description"][i]["category"]
                interest.set_category(category)

                try:
                    subcategory_list = injson["description"][i]["subcategories"]
                    interest.subcategories = []
                    for j in range(len(subcategory_list)):
                        subcategory = injson["description"][i]["subcategories"][j]
                        interest.add_subcategories(subcategory)
                except:
                    pass
                dataset.add_interests(interest)
        else:
            dataset.interests = []
        del outjson["description"]
    except Exception as e:
        pass
    try:
        favorites = Favorites()
        favorites.set_eventIds(injson["isOpenSource"]["eventIds"])
        favorites.set_placeIds(injson["isOpenSource"]["placeIds"])
        favorites.set_diningPlaceIds(injson["isOpenSource"]["diningPlaceIds"])
        favorites.set_laundryPlaceIds(injson["isOpenSource"]["laundryPlaceIds"])
        favorites.set_athleticEventIds(injson["isOpenSource"]["athleticEventIds"])
        dataset.set_favorites(favorites)
        del outjson["isOpenSource"]
    except Exception as e:
        pass
    try:
        dataset.set_positiveInterestTags(injson["apiDoc"])
        del outjson["apiDoc"]
    except:
        pass
    try:
        dataset.set_negativeInterestTags(injson["deploymentStatus"])
        del outjson["deploymentStatus"]
    except:
        pass
    try:
        privacySettings = PrivacySettings()
        level = injson["ifExternallyDeployed"]["level"]
        date_modified = injson["ifExternallyDeployed"]["dateModified"]
        privacySettings.set_level(level)
        privacySettings.set_date_modified(date_modified)

        dataset.set_privacy_settings(privacySettings)
    except Exception as e:
        pass
    try:
        dataset.set_creation_date(injson["creationDate"])
    except Exception as e:
        pass
    try:
        dataset.set_last_modified_date(injson["lastModifiedDate"])
    except Exception as e:
        pass
    try:
        del outjson["creationDate"]
        del outjson["lastModifiedDate"]
        del outjson["name"]
    except:
        pass

    return dataset, outjson

"""
set pii dataset
"""
def update_pii_dataset_from_json(dataset, injson):
    try:
        dataset.set_lastname(injson['lastname'])
    except Exception as e:
        pass
    try:
        dataset.set_firstname(injson['firstname'])
    except Exception as e:
        pass
    try:
        dataset.set_phone(injson['phone'])
    except Exception as e:
        pass
    try:
        dataset.set_email(injson['email'])
    except Exception as e:
        pass
    try:
        dataset.set_username(injson['username'])
    except Exception as e:
        pass
    try:
        dataset.set_uin(injson['uin'])
    except Exception as e:
        pass
    try:
        dataset.set_netid(injson['netid'])
    except Exception as e:
        pass
    try:
        dataset.set_creation_date(injson["creationDate"])
    except Exception as e:
        pass
    try:
        dataset.set_last_modified_date(injson["lastModifiedDate"])
    except Exception as e:
        pass

    return dataset


