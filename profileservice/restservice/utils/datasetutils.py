from profileservice.dao.interest import Interest
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


