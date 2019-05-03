import uuid as uuidlib

def update_pii_dataset_from_json(dataset, injson):
    # try:
    #     dataset.set_pii_uuid(injson["pii_uuid"])
    # except:
    #     dataset.set_pii_uuid(str(uuidlib.uuid4()))
    #     pass
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

    return dataset

# def update_non_pii_uuid(non_pii_uuid):
#     # update pii_dataset's non_pii_uuid
#         non_pii_uuid = injson["uuid"]
#         print(type(non_pii_uuid).__name__)
#         if type(non_pii_uuid).__name__ == 'list':
#             is_non_pii_uuid_in_json_new = False
#         is_non_pii_uuid_in_json_new = False
#         non_pii_uuid_from_dataset = dataset.get_uuid()
#         # if it is a new entry, non_pii_uuid_from_dataset should be none
#         if non_pii_uuid_from_dataset is None:
#             is_non_pii_uuid_in_json_new = True
#             non_pii_uuid_from_dataset = []
#         else:  # check if non-pii-uuid is already in there
#             for i in range(len(non_pii_uuid_from_dataset)):
#                 if non_pii_uuid == non_pii_uuid_from_dataset[i]:
#                     is_non_pii_uuid_in_json_new = False
#
#         # adde non-pii uuid in json only if it is now uuid
#         if is_non_pii_uuid_in_json_new:
#             non_pii_uuid_from_dataset.append(non_pii_uuid)
#
#         dataset.set_uuid(non_pii_uuid_from_dataset)
#     except Exception as e:
#         pass
#
#     return dataset


