import copy

from models.ifopensource import IfOpenSource
from models.deploymentstatus import DeploymentStatus
from models.ifextneranllydeployed import IfExternallyDeployed
from models.ifinternallydeployed import IfInternallyDeployed
from models.healthcheckurl import HealthCheckUrl
from models.status import Status
from models.datadeletionapiendpoint import DataDeletionApiEndpoint
from models.contacts import Contacts
from models.contributordetails import ContributorDetails

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
        ifOpenSource = IfOpenSource()
        sourceCodeRepositoryUrl = injson["ifOpenSource"]["sourceCodeRepositoryUrl"]
        ifOpenSource.set_soucrce_code_repository_url(sourceCodeRepositoryUrl)
        dataset.set_if_open_source(ifOpenSource)
        del outjson["isOpenSource"]
    except Exception as e:
        pass
    try:
        dataset.set_api_doc(injson['apiDoc'])
        del outjson['apiDoc']
    except:
        pass
    try:
        deploymentStatus = DeploymentStatus()
        internal = injson["deploymentStatus"]["internal"]
        external = injson["deploymentStatus"]["external"]
        deploymentStatus.set_internal(internal)
        deploymentStatus.set_internal(external)
        dataset.set_deployment_status(deploymentStatus)
        del outjson["deploymentStatus"]
    except Exception as e:
        pass
    try:
        ifExternallyDeployed = IfExternallyDeployed()
        apiUrl = injson["ifExternallyDeployed"]["apiUrl"]
        ifExternallyDeployed.set_api_url(apiUrl)
        dataset.set_if_externally_deployed(ifExternallyDeployed)
        del outjson["ifExternallyDeployed"]
    except Exception as e:
        pass
    try:
        ifInternallyDeployed = IfInternallyDeployed()
        dockerImage = injson["ifInternallyDeployed"]["dockerImage"]
        environmentalVariables = injson["ifInternallyDeployed"]["environmentalVariables"]
        databaseDetails = injson["ifInternallyDeployed"]["databaseDetails"]
        ifInternallyDeployed.set_docker_image(dockerImage)
        ifInternallyDeployed.set_environmental_variables(environmentalVariables)
        ifInternallyDeployed.set_database_details(databaseDetails)
        dataset.set_if_internally_deployed(ifInternallyDeployed)
        del outjson["ifInternallyDeployed"]
    except Exception as e:
        pass
    try:
        dataset.set_version(injson['version'])
        del outjson['version']
    except:
        pass
    try:
        healthCheckUrl = HealthCheckUrl()
        discussion = injson["healthCheckUrl"]["discussion"]
        healthCheckUrl.set_discussion(discussion)
        dataset.set_health_check_url(healthCheckUrl)
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
        inReview = injson["status"]["inReview"]
        approved = injson["status"]["approved"]
        pubulished = injson["status"]["pubulished"]
        status.set_submitted(submitted)
        status.set_in_review(inReview)
        status.set_approved(approved)
        status.set_pubulished(pubulished)
        dataset.set_status(status)
        del outjson["status"]
    except Exception as e:
        pass
    try:
        dataDeletionApiEndpoint = DataDeletionApiEndpoint()
        uuid = injson["dataDeletionApiEndpoint"]["uuid"]
        check = injson["dataDeletionApiEndpoint"]["check"]
        dataDeletionApiEndpoint.set_uuid(uuid)
        dataDeletionApiEndpoint.set_check(check)
        dataset.set_data_deletion_api_endpoint(dataDeletionApiEndpoint)
        del outjson["dataDeletionApiEndpoint"]
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
        contributorDetails = ContributorDetails()
        name = injson["contributorDetails"]["name"]
        email = injson["contributorDetails"]["email"]
        phone = injson["contributorDetails"]["phone"]
        organization = injson["contributorDetails"]["organization"]
        officialAddress = injson["contributorDetails"]["officialAddress"]
        contributorDetails.set_name(name)
        contributorDetails.set_email(email)
        contributorDetails.set_phone(phone)
        contributorDetails.set_organization(organization)
        contributorDetails.set_officialAddress(officialAddress)
        dataset.set_contributor_details(contributorDetails)
        del outjson["contributorDetails"]
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



