from bson import ObjectId


def format_query(args, query):
    query_parts = []

    if args.get('email'):
        query_parts.append({'email': {'$eq': args.get('email')}})
    if args.get('phone'):
        query_parts.append({'phone': {'$eq': args.get('phone')}})

    if query_parts:
        query['$and'] = query_parts

    return query

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

