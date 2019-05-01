import json

def remove_objectid_from_dataset(dataset):
    if "_id" in dataset:
        del dataset["_id"]

    return dataset