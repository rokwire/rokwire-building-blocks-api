import utils.datasetutils as datasetutils

class Capability():
    def __init__(self, injson):
        self.name = None
        self.description = None
        self.isOpenSource = None
        self.ifOpenSource = None
        self.apiDoc = None
        self.deploymentStatus = None
        self.ifExternallyDeployed = None
        self.ifInternallyDeployed = None
        self.version = None
        self.healthCheckUrl = None
        self.authMethod = None
        self.status = None
        self.dataDeletionApiEndpoint = None
        self.contacts = None
        self.contributorDetails = None
        self.creationDate = None
        self.lastModifiedDate = None

        self, restjson = datasetutils.update_capability_dataset_from_json(self, injson)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_is_open_source(self, isOpenSource):
        self.isOpenSource = isOpenSource

    def get_is_open_source(self):
        return self.isOpenSource

    def set_if_open_source(self, ifOpenSource):
        self.ifOpenSource = ifOpenSource

    def get_if_open_source(self):
        return self.ifOpenSource

    def set_api_doc(self, apiDoc):
        self.apiDoc = apiDoc

    def get_api_doc(self):
        return self.apiDoc

    def set_deployment_status(self, deploymentStatus):
        self.deploymentStatus = deploymentStatus

    def get_deployment_status(self):
        return self.deploymentStatus

    def set_if_externally_deployed(self, ifExternallyDeployed):
        self.ifExternallyDeployeds = ifExternallyDeployed

    def get_if_externally_deployeds(self):
        return self.ifExternallyDeployeds

    def set_if_internally_deployed(self, ifInternallyDeployed):
        self.ifInternallyDeployed = ifInternallyDeployed

    def get_if_internally_deployed(self):
        return self.ifInternallyDeployed

    def set_version(self, version):
        self.version = version

    def get_version(self):
        return self.version

    def set_health_check_url(self, healthCheckUrl):
        self.healthCheckUrl = healthCheckUrl

    def get_health_check_url(self):
        return self.healthCheckUrl

    def set_auth_method(self, authMethod):
        self.authMethod = authMethod

    def get_auth_method(self):
        return self.authMethod

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_data_deletion_api_endpoint(self, dataDeletionApiEndpoint):
        self.dataDeletionApiEndpoint = dataDeletionApiEndpoint

    def get_data_deletion_api_endpoint(self):
        return self.dataDeletionApiEndpoint

    def set_contacts(self, contacts):
        self.contacts = contacts

    def get_contacts(self):
        return self.contacts

    def set_contributor_details(self, contributorDetails):
        self.contributorDetails = contributorDetails

    def get_contributor_details(self):
        return self.contributorDetails

    def set_creation_date(self, creationDate):
        self.creationDate = creationDate

    def get_creation_date(self):
        return self.creationDate

    def set_last_modified_date(self, lastModifiedDate):
        self.lastModifiedDate = lastModifiedDate

    def get_last_modified_date(self):
        return self.lastModifiedDate