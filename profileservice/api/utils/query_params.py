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

    if args.get('eventId'):
        query_parts.append({'eventId': {'$eq': args.get('eventId')}})
    # if args.get('template'):
    #     query_parts.append({'template': {'$eq': args.get('template')}})

    if query_parts:
        query['$and'] = query_parts

    return query

