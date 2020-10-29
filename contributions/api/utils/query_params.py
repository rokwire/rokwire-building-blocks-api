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

from bson import ObjectId

def format_query_contribution(args, query):
    query_parts = []

    if args.get('id'):
        # make sure it has been changed to eventIds from eventid since the db field name is eventIds
        query_parts.append({'_id': {'$eq': ObjectId(args.get('id'))}})
    if args.get('name'):
        query_parts.append({'name': {'$eq': args.get('name')}})

    if query_parts:
        query['$and'] = query_parts

    return query

def format_query_capability(args, query):
    query_parts = []

    if args.get('name'):
        query_parts.append({'capabilities.name': {'$eq': args.get('name')}})

    if query_parts:
        query['$and'] = query_parts

    return query

def format_query_talent(args, query):
    query_parts = []

    if args.get('name'):
        query_parts.append({'talents.name': {'$eq': args.get('name')}})

    if query_parts:
        query['$and'] = query_parts

    return query

