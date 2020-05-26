import copy

from models.capabilities.contact import Contact
from models.capabilities.datadeletionendpointdetail import DataDeletionEndpointDetail
from models.capabilities.deploymentdetails import DeploymentDetails
from models.capabilities.environmentvariable import EnvironmentVariable
from models.capabilities.status import Status

"""
update contribution dataset
"""
def update_contribution_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_short_description(injson['shortDescription'])
        del outjson['shortDescription']
    except:
        pass
    try:
        dataset.set_capabilities(injson['capabilities'])
        del outjson['capabilities']
    except:
        pass
    try:
        dataset.set_talents(injson['talents'])
        del outjson['talents']
    except:
        pass
    try:
        dataset.set_date_created(injson["dateCreated"])
        del outjson["dateCreated"]
    except Exception as e:
        pass
    try:
        dataset.set_date_modified(injson["dateModified"])
        del outjson["dateModified"]
    except Exception as e:
        pass

    return dataset, outjson

"""
set capability dataset
"""
def update_capability_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_description(injson['description'])
        del outjson['description']
    except:
        pass
    try:
        dataset.set_is_open_source(injson['isOpenSource'])
        del outjson['isOpenSource']
    except:
        pass
    try:
        dataset.set_api_doc_url(injson['apiDocUrl'])
        del outjson['apiDocUrl']
    except:
        pass
    try:
        deployment_details = DeploymentDetails()
        try:
            location = injson["deploymentLocation"]["location"]
            deployment_details.set_location(location)
        except:
            pass
        try:
            docker_image_name = injson["deploymentLocation"]["dockerImageName"]
            deployment_details.set_docker_image_name(docker_image_name)
        except:
            pass
        try:
            environment_variable = EnvironmentVariable()
            key = injson["deploymentLocation"]["environmentVariable"]["key"]
            value = injson["deploymentLocation"]["environmentVariable"]["value"]
            environment_variable.set_key(key)
            environment_variable.set_value(value)
            deployment_details.set_environment_variable(environment_variable)
            del outjson["environmentVariable"]
        except Exception as e:
            pass
        try:
            database_details = injson["deploymentLocation"]["databaseDetails"]
            deployment_details.set_database_details(database_details)
        except:
            pass
        try:
            auth_method = injson["deploymentLocation"]["authMethod"]
            deployment_details.set_auth_method(auth_method)
        except:
            pass
        dataset.set_deployment_details(deployment_details)
        del outjson["deploymentLocation"]
    except Exception as e:
        pass
    try:
        dataset.set_api_base_url(injson['apiBaseUrl'])
        del outjson['apiBaseUrl']
    except:
        pass
    try:
        dataset.set_docker_image_name(injson['dockerImageName'])
        del outjson['dockerImageName']
    except:
        pass
    try:
        dataset.set_database_details(injson['databaseDetails'])
        del outjson['databaseDetails']
    except:
        pass
    try:
        dataset.set_version(injson['version'])
        del outjson['version']
    except:
        pass
    try:
        dataset.set_health_check_url(injson["healthCheckUrl"])
        del outjson["healthCheckUrl"]
    except Exception as e:
        pass
    try:
        dataset.set_auth_method(injson['authMethod'])
        del outjson['authMethod']
    except:
        pass
    try:
        status = Status()
        try:
            submitted = injson["status"]["submitted"]
            status.set_submitted(submitted)
        except:
            pass
        try:
            reviewing = injson["status"]["reviewing"]
            status.set_in_review(reviewing)
        except:
            pass
        try:
            approved = injson["status"]["approved"]
            status.set_approved(approved)
        except:
            pass
        try:
            disapproved = injson["status"]["disapproved"]
            status.set_disapproved(disapproved)
        except:
            pass
        try:
            pubulished = injson["status"]["pubulished"]
            status.set_pubulished(pubulished)
        except:
            pass
        dataset.set_status(status)
        del outjson["status"]
    except Exception as e:
        pass
    try:
        data_deletion_endpoint_detail = DataDeletionEndpointDetail()
        try:
            deletion_endpoint = injson["dataDeletionEndpointDetails"]["deletionEndpoint"]
            data_deletion_endpoint_detail.set_deletion_endpoint(deletion_endpoint)
        except:
            pass
        try:
            description = injson["dataDeletionEndpointDetails"]["description"]
            data_deletion_endpoint_detail.set_description(description)
        except:
            pass
        try:
            api_key = injson["dataDeletionEndpointDetails"]["apiKey"]
            data_deletion_endpoint_detail.set_api_key(api_key)
        except:
            pass
        dataset.set_data_deletion_endpoint_details(data_deletion_endpoint_detail)
        try:
            del outjson["dataDeletionEndpointDetails"]
        except:
            pass
    except Exception as e:
        pass
    try:
        contact = Contact()
        try:
            name = injson["contacts"]["name"]
            contact.set_name(name)
        except:
            pass
        try:
            email = injson["contacts"]["email"]
            contact.set_email(email)
        except:
            pass
        try:
            phone = injson["contacts"]["phone"]
            contact.set_phone(phone)
        except:
            pass
        try:
            organization = injson["contacts"]["organization"]
            contact.set_organization(organization)
        except:
            pass
        try:
            officialAddress = injson["contacts"]["officialAddress"]
            contact.set_officialAddress(officialAddress)
        except:
            pass
        dataset.set_contacts(contact)
        try:
            del outjson["contacts"]
        except:
            pass
    except Exception as e:
        pass
    try:
        dataset.set_creation_date(injson["creationDate"])
        del outjson["creationDate"]
    except Exception as e:
        pass
    try:
        dataset.set_last_modified_date(injson["lastModifiedDate"])
        del outjson["lastModifiedDate"]
    except Exception as e:
        pass

    return dataset, outjson