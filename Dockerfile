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

FROM swaggerapi/swagger-ui:v3.28.0

COPY appconfigservice/appconfig.yaml eventservice/events.yaml profileservice/profile.yaml loggingservice/logging.yaml /usr/share/nginx/html/app/

ENV URLS "[{url: 'app/appconfig.yaml', name: 'App Config Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/content/doc/ui/', name: 'Content Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/core/doc/ui/', name: 'Core Building Block'}, {url: 'app/events.yaml', name: 'Events Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/gr/doc/ui/', name: 'Groups Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/lms/doc/ui/', name: 'Learning Management System (LMS) Building Block'}, {url: 'app/logging.yaml', name: 'Logging Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/notifications/api/doc/ui/', name: 'Notifications Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/polls/doc/ui/', name: 'Polls Building Block'}, {url: 'app/profile.yaml', name: 'Profile Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/rewards/doc/ui/', name: 'Rewards Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/wellness/doc/ui/', name: 'Wellness Building Block'}]"

VOLUME /usr/share/nginx/html/app/

ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]
