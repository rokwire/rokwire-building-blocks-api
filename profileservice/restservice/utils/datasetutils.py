from profileservice.dao.interest import Interest
from profileservice.dao.favorites import Favorites

"""
set non pii dataset
"""
def update_non_pii_dataset_from_json(dataset, injson):
    try:
        dataset.set_file_descriptors(injson['fileDescriptors'])
    except:
        pass
    try:
        dataset.set_over13(injson['over13'])
    except:
        pass
    try:
        # check if it is a first interests
        if dataset.get_interests() is not None:
            for i in range(len(injson["interests"])):
                interest = Interest()
                category = injson["interests"][i]["category"]
                interest.set_category(category)

                try:
                    subcategory_list = injson["interests"][i]["subcategories"]
                    interest.subcategories = []
                    for j in range(len(subcategory_list)):
                        subcategory = injson["interests"][i]["subcategories"][j]
                        interest.add_subcategories(subcategory)
                except:
                    pass
                dataset.add_interests(interest)
        else:
            dataset.interests = []
    except Exception as e:
        pass
    try:
        favorites = Favorites()
        favorites.set_eventIds(injson["favorites"]["eventIds"])
        favorites.set_placeIds(injson["favorites"]["placeIds"])
        favorites.set_diningPlaceIds(injson["favorites"]["diningPlaceIds"])
        favorites.set_laundryPlaceIds(injson["favorites"]["laundryPlaceIds"])
        favorites.set_athleticEventIds(injson["favorites"]["athleticEventIds"])
        dataset.set_favorites(favorites)
    except Exception as e:
        pass
    try:
        dataset.set_interestTags(injson["interestTags"])
    except:
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


