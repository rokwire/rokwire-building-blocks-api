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

import datetime
import re
from bson import ObjectId


def format_query(args, query, include_private_events=False, group_ids=None, all_group_event=False):
    query_parts = []
    
    # isInPerson check
    is_in_person = args.get('isInPerson')
    if is_in_person:
        if is_in_person.lower() == "true":
            is_in_person = True
        else:
            is_in_person = False
        query_parts.append({'isInPerson': is_in_person})
    # group id
    group_id = args.get('groupId')
    if group_id:
        query_parts.append({'createdByGroupId': group_id})
    # superevent id
    super_event_id = args.get('superEventId')
    if super_event_id and ObjectId.is_valid(super_event_id):
        query_parts.append({'_id': ObjectId(super_event_id)})
        query_parts.append({'isSuperEvent': True})
    if args.getlist('createdBy'):
        query_parts.append({'createdBy': {'$in': args.getlist('createdBy')}})
    # multiple events ids
    if args.getlist('id'):
        ids = list()
        for event_id in args.getlist('id'):
            if ObjectId.is_valid(event_id):
                ids.append(ObjectId(event_id))
        if ids:
            query_parts.append({'_id': {'$in': ids}})
    # title text query
    if args.getlist('title'):
        titles = ' '.join(['"%s"' % t for t in args.getlist('title')])
        query_parts.append({'$text': {'$search': titles}})
    # recurrenceId query
    if args.get('recurrenceId'):
        query_parts.append({'recurrenceId': {'$eq': int(args.get('recurrenceId'))}})
    # category query
    if args.getlist('category'):
        category_main = []
        category_mainSub = []
        for category in args.getlist('category'):
            if len(category.split('.')) == 2:
                category_mainSub.append(category)
            else:
                category_main.append(category)

        # Sort the categories for better caching
        category_main = sorted(category_main)
        category_mainSub = sorted(category_mainSub)

        if category_main and category_mainSub:
            # If we have both a main and sub categories then use an $or
            # and search on both of the columns (so that indexes can
            # be used).
            query_parts.append({'$or': [
                {'category': {'$in': category_main}},
                {'categorymainsub': {'$in': category_mainSub}},
            ]})
        elif category_main:
            query_parts.append({'category': {'$in': category_main}})
        elif category_mainSub:
            query_parts.append({'categorymainsub': {'$in': category_mainSub}})
    # tags query
    if args.getlist('tags'):
        query_parts.append({'tags': {'$in': sorted(args.getlist('tags'))}})
    # target audience query
    # TODO: temporarily turn off targetAudience search
    # if args.get('targetAudience'):
    #    query['targetAudience'] = {'$in': args.getlist('targetAudience')}
    # datetime range query
    if args.get('startDate'):
        value = datetime.datetime.strptime(args.get('startDate'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the previous lowest 15min.
        value = value.replace(
            minute=(value.minute - (value.minute % 15)),
            second=0,
            microsecond=0
        )
        query_parts.append({'startDate': {'$gte': value}})
    if args.get('startDateLimit'):
        value = datetime.datetime.strptime(args.get('startDateLimit'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the previous lowest 15min.
        value = value.replace(
            minute=(value.minute - (value.minute % 15)),
            second=0,
            microsecond=0
        )
        query_parts.append({'startDate': {'$lte': value}})
    if args.get('startDate.lte'):
        value = datetime.datetime.strptime(args.get('startDate.lte'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the previous lowest 15min.
        value = value.replace(
            minute=(value.minute - (value.minute % 15)),
            second=0,
            microsecond=0
        )
        query_parts.append({'startDate': {'$lte': value}})
    if args.get('startDate.gte'):
        value = datetime.datetime.strptime(args.get('startDate.gte'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the previous lowest 15min.
        value = value.replace(
            minute=(value.minute - (value.minute % 15)),
            second=0,
            microsecond=0
        )
        query_parts.append({'startDate': {'$gte': value}})
    if args.get('endDate'):
        value = datetime.datetime.strptime(args.get('endDate'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the next highest 15min. This uses timedelta in case the
        # minute calculation turns out to be 60
        value = value + datetime.timedelta(
            minutes=((15 - value.minute) % 15),
            seconds=-value.second,
            microseconds=-value.microsecond
        )
        query_parts.append({'endDate': {'$lte': value}})
    if args.get('endDate.lte'):
        value = datetime.datetime.strptime(args.get('endDate.lte'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the next highest 15min. This uses timedelta in case the
        # minute calculation turns out to be 60
        value = value + datetime.timedelta(
            minutes=((15 - value.minute) % 15),
            seconds=-value.second,
            microseconds=-value.microsecond
        )
        query_parts.append({'endDate': {'$lte': value}})
    if args.get('endDate.gte'):
        value = datetime.datetime.strptime(args.get('endDate.gte'), "%Y-%m-%dT%H:%M:%S")
        # Clamp values to the next highest 15min. This uses timedelta in case the
        # minute calculation turns out to be 60
        value = value + datetime.timedelta(
            minutes=((15 - value.minute) % 15),
            seconds=-value.second,
            microseconds=-value.microsecond
        )
        query_parts.append({'endDate': {'$gte': value}})
    # geolocation query
    if args.get('latitude') and args.get('longitude') and args.get('radius'):
        # Round to a 100m box to improve caching
        coordinates = [
            round(float(args.get('longitude')), 3),
            round(float(args.get('latitude')), 3)
        ]
        radius_meters = int(args.get('radius'))
        query_parts.append({'coordinates': {'$geoWithin': {'$centerSphere': [coordinates, radius_meters * 0.000621371 / 3963.2]}}})

    # ApiKeyAuth query
    if not include_private_events:
        if not all_group_event:
            query_parts.append({'isGroupPrivate': {'$ne': True}})
        query['$and'] = query_parts
    # UserAuth query
    else:
        if not all_group_event:
            pubic_private_groups_access_parts = {'$or': [
                {'isGroupPrivate': {'$ne': True}},  # Includes both group public and regular public events
                {'createdByGroupId': {'$in': group_ids}}]}  # Check for group membership. Also include group private events.
            query_parts.append(pubic_private_groups_access_parts)
        query['$and'] = query_parts

    # All_group_events
    if all_group_event:
        query_parts.append({'createdByGroupId': {'$exists': True}})

    return query


def required_check(req_data):
    if req_data['startDate'] is None or req_data['title'] is None or req_data['category'] is None:
        return False
    return True


def formate_datetime(req_data):
    if req_data.get('startDate'):
        start_date = req_data.get('startDate')
        req_data['startDate'] = datetime.datetime.strptime(start_date, "%Y/%m/%dT%H:%M:%S")
    if req_data.get('endDate'):
        end_date = req_data.get('endDate')
        req_data['endDate'] = datetime.datetime.strptime(end_date, "%Y/%m/%dT%H:%M:%S")
    return req_data


def formate_location(req_data):
    if req_data.get('location'):
        loc = req_data.get('location')
        if loc.get('longitude') and loc.get('latitude'):
            req_data['coordinates'] = [loc.get('longitude'), loc.get('latitude')]
    return req_data


def formate_category(req_data):
    if req_data.get('category') and req_data.get('subcategory'):
        req_data['categorymainsub'] = req_data.get('category') + '.' + req_data.get('subcategory')
    elif req_data.get('category'):
        req_data['categorymainsub'] = req_data.get('category')
    return req_data


def update_category(req_data, data_tuple):
    if req_data.get('category') or req_data.get('subcategory'):
        category_main = ''
        category_sub = ''
        if data_tuple.get('categorymainsub'):
            category_main = data_tuple.get('categorymainsub').split('.')[0]
            if len(data_tuple.get('categorymainsub').split('.')) == 2:
                category_sub = data_tuple.get('categorymainsub').split('.')[1]
        if req_data.get('category'):
            category_main = req_data.get('category')
        if req_data.get('subcategory'):
            category_sub = req_data.get('subcategory')
        req_data['categorymainsub'] = category_main + "." + category_sub
    return req_data


def update_coordinates(req_data, coordinates):
    if req_data.get('location.latitude'):
        coordinates[1] = req_data.get('location.latitude')
        req_data['coordinates'] = coordinates

    if req_data.get('location.longitude'):
        coordinates[0] = req_data.get('location.longitude')
        req_data['coordinates'] = coordinates


def format_datetime_response(obj):
    # Example format: Fri, 27 Mar 2020 01:00:00 GMT
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%a, %d %b %Y %H:%M:%S GMT')
