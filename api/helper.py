from json import loads as loader


def loads(data):
    try:
        data = loader(data)
    except Exception:
        data = loader(data.decode('utf-8'))
    return data


def pagination_response(pagination, route):
    """Returns a pagination response that can be dump into json"""
    items = []
    for item in pagination.items:
        items.append(item.json())
    return pagination_response_items(pagination, route, items)


def pagination_response_items(pagination, route, items):
    """Returns a pagination response for the given items"""
    response = {}
    response['has_next'] = pagination.has_next
    response['has_prev'] = pagination.has_prev
    response['items'] = items

    response['next_url'] = (route + "?page={}".format(pagination.next_num)
                            if pagination.has_next
                            else None)
    response['prev_url'] = (route + "?page={}".format(pagination.prev_num)
                            if pagination.has_prev
                            else None)
    response['total'] = pagination.total
    response['pages'] = pagination.pages
    return response
