# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.1 - 2019-04-19
### Added
- creaste profile data model boiler plate.
[SCCI-103](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-103)
- created profile restservice boiler plate.
[SCCI-130](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-130)
- added time stamp
[SCCI-131](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-131)
- added age over 13
[SCCI-132](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-132)
- checking method for email and phone number to prevent duplicate entry
[#37](https://github.com/rokwire/rokwire-building-blocks-api/issues/37)
- profile rest service dockerized
[#62](https://github.com/rokwire/rokwire-building-blocks-api/issues/62)
- added favorites
[#115](https://github.com/rokwire/rokwire-building-blocks-api/issues/115)
- added positive and negative interest tags
[#116](https://github.com/rokwire/rokwire-building-blocks-api/issues/116)
- added an ability to store and retrieve schema free information
[#117](https://github.com/rokwire/rokwire-building-blocks-api/issues/117)
- added privacySettings in PII data model
[#138](https://github.com/rokwire/rokwire-building-blocks-api/issues/138)


### Changed
[SCCI-104](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-104)
- separated non-pii data and pii data
[SCCI-123](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-123)
- separated non-pii and pii database
- image update and fileDescriptor moved to pii from non-pii
[#72](https://github.com/rokwire/rokwire-building-blocks-api/issues/72)
- separated non-pii and pii database url
[#73](https://github.com/rokwire/rokwire-building-blocks-api/issues/73)
- profile building block rest api changed to Flask RESTFul api service
[#31](https://github.com/rokwire/rokwire-building-blocks-api/issues/31)
- non-pii interests has been modified with category and subcategory
[#86](https://github.com/rokwire/rokwire-building-blocks-api/issues/86)
- README file has examples for the endpoints
[#119](https://github.com/rokwire/rokwire-building-blocks-api/issues/119)
- database indexing system changed for document DB
[#127](https://github.com/rokwire/rokwire-building-blocks-api/issues/127)
- updated logging system based on Flask RESTFul service
[#130](https://github.com/rokwire/rokwire-building-blocks-api/issues/130)

### Fixed

