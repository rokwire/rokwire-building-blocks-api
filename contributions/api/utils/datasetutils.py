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

import copy

from models.contact import Contact
from models.capabilities.datadeletionendpointdetail import DataDeletionEndpointDetail
from models.capabilities.deploymentdetails import DeploymentDetails
from models.capabilities.environmentvariable import EnvironmentVariable
from models.talents.selfcertification import SelfCertification
from models.talents.requiredcapability import RequiredCapability

"""
update contribution dataset
"""
def update_contribution_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_contribution_admins(injson['contributionAdmins'])
        del outjson['contributionAdmins']
    except:
        pass
    try:
        dataset.set_short_description(injson['shortDescription'])
        del outjson['shortDescription']
    except:
        pass
    try:
        dataset.set_long_description(injson["longDescription"])
    except:
        pass
    try:
        dataset.set_contributors(injson['contributors'])
        del outjson['contributors']
    except:
        pass
    try:
        contact_list = []
        contact_json = injson['contacts']
        for i in range(len(contact_json)):
            tmp_contact = Contact()
            try:
                name = injson["contacts"][i]["name"]
                tmp_contact.set_name(name)
            except:
                pass
            try:
                email = injson["contacts"][i]["email"]
                tmp_contact.set_email(email)
            except:
                pass
            try:
                phone = injson["contacts"][i]["phone"]
                tmp_contact.set_phone(phone)
            except:
                pass
            try:
                organization = injson["contacts"][i]["organization"]
                tmp_contact.set_organization(organization)
            except:
                pass
            try:
                officialAddress = injson["contacts"][i]["officialAddress"]
                tmp_contact.set_officialAddress(officialAddress)
            except:
                pass
            contact_list.append(tmp_contact)
        dataset.set_contacts(contact_list)
        try:
            del outjson["contacts"]
        except:
            pass
    except Exception as e:
        pass
    try:
        dataset.set_capabilities(injson['capabilities'])
        del outjson['capabilities']
    except:
        pass
    try:
        dataset.set_talents(injson['talents'])
        del outjson['talents']
    except:
        pass
    try:
        dataset.set_review(injson['review'])
        del outjson['review']
    except:
        pass
    try:
        dataset.set_status(injson["status"])
        del outjson["status"]
    except Exception as e:
        pass
    try:
        dataset.set_date_created(injson["dateCreated"])
        del outjson["dateCreated"]
    except Exception as e:
        pass
    try:
        dataset.set_date_modified(injson["dateModified"])
        del outjson["dateModified"]
    except Exception as e:
        pass

    return dataset, outjson

"""
set capability dataset
"""
def update_capability_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_id(injson['id'])
        del outjson['id']
    except:
        pass
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_description(injson['description'])
        del outjson['description']
    except:
        pass
    try:
        dataset.set_icon(injson['icon'])
        del outjson['icon']
    except:
        pass
    try:
        dataset.set_is_open_source(injson['isOpenSource'])
        del outjson['isOpenSource']
    except:
        pass
    try:
        dataset.set_source_repo_url(injson['sourceRepoUrl'])
        del outjson['sourceRepoUrl']
    except:
        pass
    try:
        dataset.set_api_doc_url(injson['apiDocUrl'])
        del outjson['apiDocUrl']
    except:
        pass
    try:
        deployment_details = DeploymentDetails()
        try:
            location = injson["deploymentDetails"]["location"]
            deployment_details.set_location(location)
        except:
            pass
        try:
            docker_image_name = injson["deploymentDetails"]["dockerImageName"]
            deployment_details.set_docker_image_name(docker_image_name)
        except:
            pass
        try:
            env_var_list = []
            in_env_var_list = injson["deploymentDetails"]["environmentVariables"]
            for env_var in in_env_var_list:
                environment_variable = EnvironmentVariable()
                key = env_var["key"]
                value = env_var["value"]
                # check if non-empty key
                if key:
                    environment_variable.set_key(key)
                    environment_variable.set_value(value)
                    env_var_list.append(environment_variable)
            deployment_details.set_environment_variables(env_var_list)
            del outjson["environmentVariables"]
        except Exception as e:
            pass
        try:
            database_details = injson["deploymentDetails"]["databaseDetails"]
            deployment_details.set_database_details(database_details)
        except:
            pass
        try:
            auth_method = injson["deploymentDetails"]["authMethod"]
            deployment_details.set_auth_method(auth_method)
        except:
            pass
        dataset.set_deployment_details(deployment_details)
        del outjson["deploymentDetails"]
    except Exception as e:
        pass
    try:
        dataset.set_api_base_url(injson['apiBaseUrl'])
        del outjson['apiBaseUrl']
    except:
        pass
    try:
        dataset.set_docker_image_name(injson['dockerImageName'])
        del outjson['dockerImageName']
    except:
        pass
    try:
        dataset.set_database_details(injson['databaseDetails'])
        del outjson['databaseDetails']
    except:
        pass
    try:
        dataset.set_version(injson['version'])
        del outjson['version']
    except:
        pass
    try:
        dataset.set_version_url(injson['versionUrl'])
        del outjson['versionUrl']
    except:
        pass
    try:
        dataset.set_health_check_url(injson["healthCheckUrl"])
        del outjson["healthCheckUrl"]
    except Exception as e:
        pass
    try:
        dataset.set_auth_method(injson['authMethod'])
        del outjson['authMethod']
    except:
        pass
    try:
        data_deletion_endpoint_detail = DataDeletionEndpointDetail()
        try:
            deletion_endpoint = injson["dataDeletionEndpointDetails"]["deletionEndpoint"]
            data_deletion_endpoint_detail.set_deletion_endpoint(deletion_endpoint)
        except:
            pass
        try:
            description = injson["dataDeletionEndpointDetails"]["description"]
            data_deletion_endpoint_detail.set_description(description)
        except:
            pass
        try:
            api_key = injson["dataDeletionEndpointDetails"]["apiKey"]
            data_deletion_endpoint_detail.set_api_key(api_key)
        except:
            pass
        dataset.set_data_deletion_endpoint_details(data_deletion_endpoint_detail)
        try:
            del outjson["dataDeletionEndpointDetails"]
        except:
            pass
    except Exception as e:
        pass
    try:
        dataset.set_creation_date(injson["creationDate"])
        del outjson["creationDate"]
    except Exception as e:
        pass
    try:
        dataset.set_last_modified_date(injson["lastModifiedDate"])
        del outjson["lastModifiedDate"]
    except Exception as e:
        pass

    return dataset, outjson

"""
update person dataset
"""
def update_person_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_contributor_type(injson['contributorType'])
        del outjson['contributorType']
    except:
        pass
    try:
        dataset.set_first_name(injson['firstName'])
        del outjson['firstName']
    except:
        pass
    try:
        dataset.set_middle_name(injson['middleName'])
        del outjson['middleName']
    except:
        pass
    try:
        dataset.set_last_name(injson['lastName'])
        del outjson['lastName']
    except:
        pass
    try:
        dataset.set_email(injson['email'])
        del outjson['email']
    except:
        pass
    try:
        dataset.set_phone(injson["phone"])
        del outjson['email']
    except:
        pass
    try:
        dataset.set_affiliation(injson['affiliation'])
        del outjson['affiliation']
    except:
        pass

    return dataset, outjson

"""
update organization dataset
"""
def update_organization_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_contributor_type(injson['contributorType'])
        del outjson['contributorType']
    except:
        pass
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_address(injson['address'])
        del outjson['address']
    except:
        pass
    try:
        dataset.set_email(injson['email'])
        del outjson['email']
    except:
        pass
    try:
        dataset.set_phone(injson["phone"])
        del outjson['email']
    except:
        pass

    return dataset, outjson

"""
set talent dataset
"""
def update_talent_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_id(injson['id'])
        del outjson['id']
    except:
        pass
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_icon(injson['icon'])
        del outjson['icon']
    except:
        pass
    try:
        dataset.set_short_description(injson['shortDescription'])
        del outjson['shortDescription']
    except:
        pass
    try:
        dataset.set_long_description(injson['longDescription'])
        del outjson['longDescription']
    except:
        pass
    try:
        required_capabilities_json = injson['requiredCapabilities']
        required_capabilities_list = []
        for required_capability_json in required_capabilities_json:
            required_capability_dataset = None
            required_capability_dataset = update_required_capability_dataset_from_json(required_capability_dataset, required_capability_json)
            if required_capability_dataset is not None:
                required_capabilities_list.append(required_capability_dataset)
        dataset.set_required_capabilities(injson['requiredCapabilities'])
        del outjson['requiredCapabilities']
    except:
        pass
    try:
        dataset.set_required_building_blocks(injson['requiredBuildingBlocks'])
        del outjson['requiredBuildingBlocks']
    except:
        pass
    try:
        dataset.set_min_user_privacy_level(injson['minUserPrivacyLevel'])
        del outjson['minUserPrivacyLevel']
    except:
        pass
    try:
        dataset.set_min_end_user_roles(injson['minEndUserRoles'])
        del outjson['minEndUserRoles']
    except:
        pass
    try:
        dataset.set_start_date(injson['startDate'])
        del outjson['startDate']
    except:
        pass
    try:
        dataset.set_end_date(injson['endDate'])
        del outjson['endDate']
    except:
        pass
    try:
        dataset.set_data_description(injson['dataDescription'])
        del outjson['dataDescription']
    except:
        pass
    try:
        self_certification = SelfCertification()
        try:
            data_deleteion_upon_request = injson["selfCertification"]["dataDeletionUponRequest"]
            self_certification.set_data_deletion_upon_request(data_deleteion_upon_request)
        except:
            pass
        try:
            respecting_user_privacy_setting = injson["selfCertification"]["respectingUserPrivacySetting"]
            self_certification.set_respecting_user_privacy_setting(respecting_user_privacy_setting)
        except:
            pass
        try:
            disclose_ads = injson["selfCertification"]["discloseAds"]
            self_certification.set_disclose_ads(disclose_ads)
        except:
            pass
        try:
            disclose_sponsors = injson["selfCertification"]["discloseSponsors"]
            self_certification.set_disclose_sponsors(disclose_sponsors)
        except:
            pass
        try:
            disclose_image_rights = injson["selfCertification"]["discloseImageRights"]
            self_certification.set_disclose_image_rights(disclose_image_rights)
        except:
            pass
        dataset.set_self_certification(self_certification)
        try:
            del outjson["selfCertification"]
        except:
            pass
    except Exception as e:
        pass

    return dataset, outjson

"""
update review dataset
"""
def update_review_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_reviewer_id(injson['reviewerId'])
        del outjson['reviewerId']
    except:
        pass
    try:
        dataset.set_review_comment(injson['reviewComment'])
        del outjson['reviewComment']
    except:
        pass
    try:
        dataset.set_review_comment(injson['reviewLastUpdate'])
        del outjson['reviewLastUpdated']
    except:
        pass

    return dataset, outjson

"""
update required capability dataset
"""
def update_required_capability_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_contribution_id(injson['contributionId'])
        del outjson['contributionId']
    except:
        pass
    try:
        dataset.set_capability_id(injson['capabilityId'])
        del outjson['capabilityId']
    except:
        pass
    try:
        dataset.set_capability_name(injson['capabilityName'])
        del outjson['capabilityName']
    except:
        pass

    return dataset, outjson

"""
update reviewer dataset
"""
def update_reviwer_dataset_from_json(dataset, injson):
    outjson = copy.copy(injson)
    try:
        dataset.set_name(injson['name'])
        del outjson['name']
    except:
        pass
    try:
        dataset.set_github_username(injson['githubUsername'])
        del outjson['githubUsername']
    except:
        pass
    try:
        dataset.set_email(injson['email'])
        del outjson['email']
    except:
        pass

    return dataset, outjson
