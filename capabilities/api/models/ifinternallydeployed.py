class IfInternallyDeployed():
    def __init__(self):
        self.dockerImage = None
        self.environmentalVariables = None
        self.databaseDetails = None

    def set_docker_image(self, dockerImage):
        self.dockerImage = dockerImage

    def get_docker_image(self):
        return self.dockerImage

    def set_environmental_variables(self, environmentalVariables):
        self.environmentalVariables = environmentalVariables

    def get_environmental_variables(self):
        return self.environmentalVariables

    def set_database_details(self, databaseDetails):
        self.databaseDetails = databaseDetails

    def get_database_details(self):
        return self.databaseDetails

