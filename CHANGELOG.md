# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add environment variable to set url prefix for the connexion events building block.
- Add super events tag to refactoring branch.
- Get events by multiple event ids.
- Add dnspython module to enable mongodb+srv:// URIs [#235](https://github.com/rokwire/rokwire-building-blocks-api/issues/235)
- API design changes to support super events. [#302](https://github.com/rokwire/rokwire-building-blocks-api/issues/302)
- Add an optional `upgrade` object in app config [#328](https://github.com/rokwire/rokwire-building-blocks-api/issues/328)
- Add a method to auth_middleware library for doing authorization. [#342](https://github.com/rokwire/rokwire-building-blocks-api/issues/342)
- Add a base path to logging and profiles service. [#362](https://github.com/rokwire/rokwire-building-blocks-api/issues/362)
- Add a base path to appconfig service. [#364](https://github.com/rokwire/rokwire-building-blocks-api/issues/364)
- Add error handlers in posting PII. [#376](https://github.com/rokwire/rokwire-building-blocks-api/issues/376)
- Add endpoint for filtering non-pii data by using eventIds. [#391](https://github.com/rokwire/rokwire-building-blocks-api/issues/391)
- Add nullable to several non-pii fields. [#398](https://github.com/rokwire/rokwire-building-blocks-api/issues/398)
### Fixed
- Issue with incompatible Python and Connexion version in Authentication Building Block. [#389](https://github.com/rokwire/rokwire-building-blocks-api/issues/389)
- Issue with date time format in event response. [#402](https://github.com/rokwire/rokwire-building-blocks-api/issues/402)

## [1.0.6] - 2020-02-25
### Added
- Compatibility in Profile PII's UUID for string and list [#372](https://github.com/rokwire/rokwire-building-blocks-api/issues/372)

### Fixed
- Profile PII PUT endpoint related to updating UUID list [#372](https://github.com/rokwire/rokwire-building-blocks-api/issues/372)

## [1.0.5] - 2020-02-05
### Added
- Add super event tags. 
- Add super event tags endpoint into rokwire.yaml file.

### Fixed
- Super events operation Id.

## [1.0.4] - 2020-01-17
### Added
- API design and code changes to support super events. [#302](https://github.com/rokwire/rokwire-building-blocks-api/issues/302)

## [1.0.3] - 2019-12-06
### Added
- Get events by multiple event ids.
- Add dnspython module to enable mongodb+srv:// URIs [#235](https://github.com/rokwire/rokwire-building-blocks-api/issues/235)

### Changed
- Update Events Service Readme to add CACHE_DIRECTORY. [#275](https://github.com/rokwire/rokwire-building-blocks-api/issues/275)
- Refactored Profile building block using connexion. [#284](https://github.com/rokwire/rokwire-building-blocks-api/issues/284)
- Update release script to build and push refactoring branch docker image. [#308](https://github.com/rokwire/rokwire-building-blocks-api/issues/308)
- Refactored App Config building block using connexion. [#294](https://github.com/rokwire/rokwire-building-blocks-api/issues/294)
- Refactored Events Building Block using connexion. [#296](https://github.com/rokwire/rokwire-building-blocks-api/issues/296)
- Set App Config Building Block's debug flag to false by default. [#332](https://github.com/rokwire/rokwire-building-blocks-api/issues/332)
- UUID entry for posting new PII dataset changed to list from string. [#329](https://github.com/rokwire/rokwire-building-blocks-api/issues/329)
- Update authorization calls in refactored Events, Profile, and App Config building blocks. [#342](https://github.com/rokwire/rokwire-building-blocks-api/issues/342)

## [1.0.2] - 2019-10-30
### Changed
- Updated version number and server URLs in API definition. [#269](https://github.com/rokwire/rokwire-building-blocks-api/issues/269)

## [1.0.1] - 2019-10-30
### Fixed
- Updated CHANGELOGs with release information. [#256](https://github.com/rokwire/rokwire-building-blocks-api/issues/265)

## [1.0.0] - 2019-10-10
### Added
- Add Docker env for AWS fargate deploy
- Add recurring event search
- Add events multiple titles search.
- Add skip and limit on events query.
- This CHANGELOG file
- Events Building Block.
- Issue template.
- Definitions for PUT method for events in YAML file.
- Fields to event schema for storing submission status and date modified.
- Scripts for deploying Swagger docker to host Rokwire API document on AWS
- Profile Building Block
- Added time stamp
- Checking method for email and phone number to prevent duplicate entry
- Profile rest service dockerized
- Image update and fileDescriptor moved to pii from non-pii
- Test profiles building block rest service deployed in AWS server
- Add searching by mobile app version feature to App Config API
- Add secretKeys to App Config
- Logging building block API definitions.
- Auth middleware library.
- Dockerfile for Rokwire Platform API documentation and updated README.
- Add caching to app-config and events GET endpoints.
- Create profile data model boiler plate. [SCCI-103](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-103)
- Created profile restservice boiler plate. [SCCI-130](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-130)
- Added time stamp. [SCCI-131](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-131)
- Added age over 13. [SCCI-132](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-132)
- Checking method for email and phone number to prevent duplicate entry. [#37](https://github.com/rokwire/rokwire-building-blocks-api/issues/37)
- Profile rest service dockerized. [#62](https://github.com/rokwire/rokwire-building-blocks-api/issues/62)
- Added favorites. [#115](https://github.com/rokwire/rokwire-building-blocks-api/issues/115)
- Added positive and negative interest tags. [#116](https://github.com/rokwire/rokwire-building-blocks-api/issues/116)
- Added an ability to store and retrieve schema free information. [#117](https://github.com/rokwire/rokwire-building-blocks-api/issues/117)
- Added privacySettings in PII data model. [#138](https://github.com/rokwire/rokwire-building-blocks-api/issues/138)
- created initial logging building block end point. [#61](https://github.com/rokwire/rokwire-building-blocks-api/issues/61)
- created a sample logging data. [#173](https://github.com/rokwire/rokwire-building-blocks-api/issues/173)

### Changed
- download events image file from S3 without checking the image id from db.
- add events building block S3 folder as env variable.
- events tag search has been changed to logic or.
- Update events schema to remove endDate as required field and add createdBy and createDate.
- Update events schema according to discussion and feedback.
- Update rokwire.yaml for events build block.
- Update rokwire.yaml for API endpoint authentication.
- Update README to include how to view Rokwire API document using Swagger
- The code repository name to rokwire-building-blocks-api.
- Fix README to use updated API definition YAML file URL.
- Fix API definition YAML file to use rokwire instead of SCCI.
- Add App Config API definition to Swagger YAML file
- Events building block API definition and schema to include event categories and sub categories
- Separated non-pii data and pii data and database in profile building block
- Profile building block rest api changed to Flask RESTFul api service
- Profile building block non-pii interests has been changed by using category and subcategory
- Update rokwire.yaml for images entry points of events building block
- Temporarily ignoring `targetAudience` search query string in events.
- Changed api doc path from http://.../api/docs to http://.../docs since our domain api.rokwire.illinois.edu contains "api" word.
- Update Events schema to include registrationLabel
- Gunicorn gevent worker class to increase performance.
- Make better use of event category indexes for performance.
- Sort events by startDate and then endDate.
- Switch profile service to use gunicorn.
- Redirect events images to S3 instead of trying to serve them directly.
- Separated non-pii data and pii data
- Separated non-pii and pii database
- Image update and fileDescriptor moved to pii from non-pii
- Separated non-pii data and pii data. [SCCI-104](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-104)
- Separated non-pii and pii database. [SCCI-123](https://opensource.ncsa.illinois.edu/jira/browse/SCCI-123)
- Image update and fileDescriptor moved to pii from non-pii. [#72](https://github.com/rokwire/rokwire-building-blocks-api/issues/72)
- Separated non-pii and pii database url. [#73](https://github.com/rokwire/rokwire-building-blocks-api/issues/73)
- Profile building block rest api changed to Flask RESTFul api service. [#31](https://github.com/rokwire/rokwire-building-blocks-api/issues/31)
- Non-pii interests has been modified with category and subcategory. [#86](https://github.com/rokwire/rokwire-building-blocks-api/issues/86)
- README file has examples for the endpoints. [#119](https://github.com/rokwire/rokwire-building-blocks-api/issues/119)
- Database indexing system changed for document DB. [#127](https://github.com/rokwire/rokwire-building-blocks-api/issues/127)
- Updated logging system based on Flask RESTFul service. [#130](https://github.com/rokwire/rokwire-building-blocks-api/issues/130)
- Made profile building block flask using the flask server configuration. [#92](https://github.com/rokwire/rokwire-building-blocks-api/issues/92)
- Modified profiles building block's rest endpoint prefix to environmental variable. [#187](https://github.com/rokwire/rokwire-building-blocks-api/issues/197)
- Modified profiles building block's log to show the endpoint information. [#244](https://github.com/rokwire/rokwire-building-blocks-api/issues/244)
- Created a method for checking the id information by comparing id token and db information. [#66](https://github.com/rokwire/rokwire-building-blocks-api/issues/66)
- Information in the id token is used for creating and updating the pii dataset. [#257](https://github.com/rokwire/rokwire-building-blocks-api/issues/257)
- URL prefix to be configurable. [#181](https://github.com/rokwire/rokwire-building-blocks-api/issues/181)
- All log entries are inserted in one database call.

### Fixed
- Events building block API definition to improve text.
- API documentation in YAML file to reflect the latest code and made text improvements.
- Issues with API specification YAML file related to app config building block.
- Indentation issues with API specification YAML file
- MongoClient use in several blocks broke connection pooling
- Don't send clickstream logs through the logging library

### Removed
- References to AWS keys and variables in the Events Building Block.

[Unreleased]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.6...HEAD
[1.0.6]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.5...1.0.6
[1.0.5]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/rokwire/rokwire-building-blocks-api/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/rokwire/rokwire-building-blocks-api/releases/tag/1.0.0
