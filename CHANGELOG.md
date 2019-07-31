# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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

### Changed
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

### Fixed
- Events building block API definition to improve text.
- API documentation in YAML file to reflect the latest code and made text improvements.
