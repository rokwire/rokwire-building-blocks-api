# class for modeling App config resource object
class AppConfigDTO:
    
    def __init__(self, id = None, mobileAppVersion = None, platformBuildingBlocks = None, thirdPartyServices = None, otherUniversityServices = None):
        self._id = id
        self._mobileAppVersion = mobileAppVersion
        self._platformBuildingBlocks = platformBuildingBlocks
        self._thirdPartyServices = thirdPartyServices
        self._otherUniversityServices = otherUniversityServices
    
    def setId(self, id):
        self._id = id
    
    def setMobileAppVersion(self, mobileAppVersion):
        self._mobileAppVersion = mobileAppVersion
        
    def setPlatformBuildingBlocks(self, platformBuildingBlocks):
        self._platformBuildingBlocks = platformBuildingBlocks
    
    def setThirdPartyServices(self, thirdPartyServices):
        self._thirdPartyServices = thirdPartyServices
    
    def setOtherUniversityServices(self, otherUniversityServices):
        self._otherUniversityServices = otherUniversityServices
        
    def getId(self):
        return self._id
        
    def getMobileAppVersion(self):
        return self._mobileAppVersion
        
    def getPlatformBuildingBlocks(self):
        return self._platformBuildingBlocks
        
    def getThirdPartyServices(self):
        return self._thirdPartyServices
        
    def getOtherUniversityServices(self):
        return self._otherUniversityServices
        
    
        
    
        
    
    
    
    