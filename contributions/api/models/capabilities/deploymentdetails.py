#  Copyright (c) 2020 by the Board of Trustees of the University of Illinois
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

class DeploymentDetails():
    def __init__(self):
        self.location = None
        self.dockerImageName = None
        self.environmentVariables = None
        self.databaseDetails = None
        self.authMethod = None

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

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

    def set_auth_method(self, authMethod):
        self.authMethod = authMethod

    def get_auth_method(self):
        return self.authMethod