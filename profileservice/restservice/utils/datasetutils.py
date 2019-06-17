
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
        dataset.set_image_url(injson['imageUrl'])
    except:
        pass
    try:
        # check if it is a first interests
        interests_num = len(dataset.get_interests)
        if interests_num > 1:
            dataset.interest.set_category(injson["interests"]["category"])
            subcat_num = len(injson["interests"]["subcategory"])
            dataset.interest.add_subcategories(injson["interests"]["subcategory"])
            dataset.add_interests(dataset.interest)
        else:
            dataset.set_interests = []
            dataset.interest.set_category(injson["interests"]["category"])
            subcat_num = len(injson["interests"]["subcategory"])
            dataset.interest.add_subcategories(injson["interests"]["subcategory"])
            dataset.add_interests(dataset.interest)
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


