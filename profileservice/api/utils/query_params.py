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

def format_query(args, query):
    query_parts = []

    if args.get('email'):
        query_parts.append({'email': {'$eq': args.get('email')}})
    if args.get('phone'):
        query_parts.append({'phone': {'$eq': args.get('phone')}})

    if query_parts:
        query['$and'] = query_parts

    return query

def format_query_device_data(args, query):
    query_parts = []

    if args.get('favorites.eventId'):
        # make sure it has been changed to eventIds from eventid since the db field name is eventIds
        query_parts.append({'favorites.eventIds': {'$eq': args.get('favorites.eventId')}})
    # if args.get('template'):
    #     query_parts.append({'template': {'$eq': args.get('template')}})

    if query_parts:
        query['$and'] = query_parts

    return query

