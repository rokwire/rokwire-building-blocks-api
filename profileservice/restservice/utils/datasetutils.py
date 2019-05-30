
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
        dataset.set_image_uri(injson['imageUrl'])
    except:
        pass
    try:
        dataset.set_general_interests(injson["generalInterests"])
    except Exception as e:
        pass
    try:
        dataset.set_athletics_interests(injson["athleticsInterests"])
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


