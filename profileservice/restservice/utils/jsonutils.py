import json

def remove_objectid_from_dataset(dataset):
    if "_id" in dataset:
        del dataset["_id"]

    return dataset

def remove_file_descriptor_from_dataset(dataset):
    if "fileDescriptors" in dataset:
        del dataset["fileDescriptors"]

    return dataset

def remove_file_descriptor_from_data_list(data_list):
    for i in range(len(data_list)):
        del data_list[i]["fileDescriptors"]

    return data_list

def remove_null_subcategory(injson):
    interests = injson["interests"]
    for i in range(len(interests)):
        interest = interests[i]
        subcategories = interest["subcategories"]
        if subcategories is None:
            del interest['subcategories']

    return interests