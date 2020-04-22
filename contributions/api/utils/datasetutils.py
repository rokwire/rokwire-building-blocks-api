import copy

from models.capabilities.contact import Contact
from models.capabilities.datadeletionendpointdetail import DataDeletionEndpointDetail
from models.capabilities.deploymentlocation import DeploymentLocation
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
        deployment_location = DeploymentLocation()
        internal = injson["deploymentLocation"]["internal"]
        external = injson["deploymentLocation"]["external"]
        deployment_location.set_internal(internal)
        deployment_location.set_internal(external)
        dataset.set_deployment_status(deployment_location)
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
        environment_variable = EnvironmentVariable()
        key = injson["deploymentLocation"]["key"]
        value = injson["deploymentLocation"]["value"]
        environment_variable.set_internal(key)
        environment_variable.set_internal(value)
        dataset.set_deployment_status(environment_variable)
        del outjson["deploymentLocation"]
    except Exception as e:
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
        submitted = injson["status"]["submitted"]
        reviewing = injson["status"]["reviewing"]
        approved = injson["status"]["approved"]
        disapproved = injson["status"]["disapproved"]
        pubulished = injson["status"]["pubulished"]
        status.set_submitted(submitted)
        status.set_in_review(reviewing)
        status.set_approved(approved)
        status.set_disapproved(disapproved)
        status.set_pubulished(pubulished)
        dataset.set_status(status)
        del outjson["status"]
    except Exception as e:
        pass
    try:
        data_deletion_endpoint_detail = DataDeletionEndpointDetail()
        deletion_endpoint = injson["dataDeletionEndpointDetails"]["deletionEndpoint"]
        api_key = injson["dataDeletionEndpointDetails"]["apiKey"]
        data_deletion_endpoint_detail.set_uuid(deletion_endpoint)
        data_deletion_endpoint_detail.set_check(api_key)
        dataset.set_data_deletion_endpoint_details(data_deletion_endpoint_detail)
        del outjson["dataDeletionEndpointDetails"]
    except Exception as e:
        pass
    try:
        contact = Contact()
        name = injson["contacts"]["name"]
        email = injson["contacts"]["email"]
        phone = injson["contacts"]["phone"]
        organization = injson["contacts"]["organization"]
        officialAddress = injson["contacts"]["officialAddress"]
        contact.set_name(name)
        contact.set_email(email)
        contact.set_phone(phone)
        contact.set_organization(organization)
        contact.set_officialAddress(officialAddress)
        dataset.set_contacts(contact)
        del outjson["contacts"]
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