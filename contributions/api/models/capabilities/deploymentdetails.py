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