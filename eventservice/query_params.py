import datetime
import re


def format_query(args, query):
    # title text query
    if args.getlist('title'):
        titles = ''
        for title in args.getlist('title'):
            titles += "\"%s\" " % title
        query['$text'] = {'$search': titles}
    # recurrenceId query
    if args.get('recurrenceId'):
        query['recurrenceId'] = {'$eq': int(args.get('recurrenceId'))}
    # category query
    if args.getlist('category'):
        category_query = list()
        for category in args.getlist('category'):
            if len(category.split('.')) == 2:
                category_query.append(category)
            else:
                wildcard = re.compile("^" + category.split('.')[0] + ".*")
                category_query.append(wildcard)
        query['categorymainsub'] = {'$in': category_query}
    # tags query
    if args.getlist('tags'):
        query['tags'] = {'$all': args.getlist('tags')}
    # target audience query
    # TODO: temporarily turn off targetAudience search
    # if args.get('targetAudience'):
    #    query['targetAudience'] = {'$in': args.getlist('targetAudience')}
    # datetime range query
    if args.get('startDate'):
        query['startDate'] = {'$gte': datetime.datetime.strptime(args.get('startDate'), "%Y-%m-%dT%H:%M:%S")}
    if args.get('endDate'):
        query['endDate'] = {'$lte': datetime.datetime.strptime(args.get('endDate'), "%Y-%m-%dT%H:%M:%S")}
    # geolocation query
    if args.get('latitude') and args.get('longitude') and args.get('radius'):
        coordinates = [float(args.get('longitude')), float(args.get('latitude'))]
        radius_meters = int(args.get('radius'))
        query['coordinates'] = {'$geoWithin': {'$centerSphere': [coordinates, radius_meters * 0.000621371 / 3963.2]}}
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
