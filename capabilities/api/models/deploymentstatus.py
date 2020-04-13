class DeploymentStatus():
    def __init__(self):
        self.internal = None
        self.external = None

    def set_internal(self, internal):
        self.internal = internal

    def get_internal(self):
        return self.internal

    def set_external(self, external):
        self.external = external

    def get_external(self):
        return self.external