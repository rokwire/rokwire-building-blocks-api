import copy

from models.contacts import Contacts
from models.datadeletionendpointdetails import DataDeletionEndpointDetails
from models.deploymentlocation import DeploymentLocation
from models.environmentvariables import EnvironmentVariables
from models.status import Status

"""
set non pii dataset
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
        environment_variables = DeploymentLocation()
        internal = injson["deploymentLocation"]["internal"]
        external = injson["deploymentLocation"]["external"]
        environment_variables.set_internal(internal)
        environment_variables.set_internal(external)
        dataset.set_deployment_status(environment_variables)
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
        environment_variables = EnvironmentVariables()
        key = injson["deploymentLocation"]["key"]
        value = injson["deploymentLocation"]["value"]
        environment_variables.set_internal(key)
        environment_variables.set_internal(value)
        dataset.set_deployment_status(environment_variables)
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
        data_deletion_endpoint_details = DataDeletionEndpointDetails()
        deletion_endpoint = injson["dataDeletionEndpointDetails"]["deletionEndpoint"]
        api_key = injson["dataDeletionEndpointDetails"]["apiKey"]
        data_deletion_endpoint_details.set_uuid(deletion_endpoint)
        data_deletion_endpoint_details.set_check(api_key)
        dataset.set_data_deletion_endpoint_details(data_deletion_endpoint_details)
        del outjson["dataDeletionEndpointDetails"]
    except Exception as e:
        pass
    try:
        contacts = Contacts()
        name = injson["contacts"]["name"]
        email = injson["contacts"]["email"]
        phone = injson["contacts"]["phone"]
        organization = injson["contacts"]["organization"]
        officialAddress = injson["contacts"]["officialAddress"]
        contacts.set_name(name)
        contacts.set_email(email)
        contacts.set_phone(phone)
        contacts.set_organization(organization)
        contacts.set_officialAddress(officialAddress)
        dataset.set_contacts(contacts)
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



