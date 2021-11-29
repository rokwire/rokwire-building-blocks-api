#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import utils.datasetutils as datasetutils

class Capability():
    def __init__(self, injson):
        self.id = None
        self.name = None
        self.description = None
        self.isOpenSource = None
        self.apiDocUrl = None
        self.deploymentDetails = None
        self.apiBaseUrl = None
        self.version = None
        self.versionUrl = None
        self.healthCheckUrl = None
        self.dataDeletionEndpointDetails = None
        # self.creationDate = None
        # self.lastModifiedDate = None

        self, restjson = datasetutils.update_capability_dataset_from_json(self, injson)

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

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

    def set_api_doc_url(self, apiDocUrl):
        self.apiDocUrl = apiDocUrl

    def get_api_doc_url(self):
        return self.apiDocUrl

    def set_deployment_details(self, deploymentDetails):
        self.deploymentDetails = deploymentDetails

    def get_deployment_details(self):
        return self.deploymentDetails

    def set_docker_image_name(self, dockerImageName):
        self.dockerImageName = dockerImageName

    def get_docker_image_name(self):
        return self.dockerImageName

    def set_environment_variables(self, environmentVariables):
        self.environmentVariables = environmentVariables

    def get_environment_variables(self):
        return self.environmentVariables

    def set_database_details(self, databaseDetails):
        self.databaseDetails = databaseDetails

    def get_database_details(self):
        return self.databaseDetails

    def set_version(self, version):
        self.version = version

    def get_version(self):
        return self.version

    def set_version_url(self, versionUrl):
        self.versionUrl = versionUrl

    def get_version_url(self):
        return self.versionUrl

    def set_health_check_url(self, healthCheckUrl):
        self.healthCheckUrl = healthCheckUrl

    def get_health_check_url(self):
        return self.healthCheckUrl

    def set_auth_method(self, authMethod):
        self.authMethod = authMethod

    def get_auth_method(self):
        return self.authMethod

    def set_data_deletion_endpoint_details(self, dataDeletionEndpointDetails):
        self.dataDeletionEndpointDetails = dataDeletionEndpointDetails

    def get_data_deletion_endpoint_details(self):
        return self.dataDeletionEndpointDetails

    # def set_creation_date(self, creationDate):
    #     self.creationDate = creationDate
    #
    # def get_creation_date(self):
    #     return self.creationDate
    #
    # def set_last_modified_date(self, lastModifiedDate):
    #     self.lastModifiedDate = lastModifiedDate
    #
    # def get_last_modified_date(self):
    #     return self.lastModifiedDate
