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

