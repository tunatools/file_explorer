
def in_bbox(obj, lat_min=None, lat_max=None, lon_min=None, lon_max=None, **kwargs):
    if not (obj.attributes.get('lat') and obj.attributes.get('lon')):
        return None
    lat = float(obj.attributes.get('lat'))
    lon = float(obj.attributes.get('lon'))
    if lat_min and lat_min > lat:
        return False
    if lat_max and lat_max < lat:
        return False
    if lon_min and lon_min > lon:
        return False
    if lon_max and lon_max < lon:
        return False
    return True


def in_time_span(obj, before=None, before_equal=None, after=None, after_equal=None, **kwargs):
    dtime = obj.attributes.get('datetime')
    if not dtime:
        return None
    if before and before <= dtime:
        return False
    if before_equal and before_equal < dtime:
        return False
    if after and after >= dtime:
        return False
    if after_equal and after_equal > dtime:
        return False
    return True


def is_matching(obj, **kwargs):
    kc_ = False
    in_ = False
    if not in_bbox(obj, **kwargs):
        return False
    if not in_time_span(obj, **kwargs):
        return False

    for key, value in kwargs.items():
        if 'KC_' in key:
            key = key.replace('KC_', '')
            kc_ = True
        if 'IN_' in key:
            key = key.replace('IN_', '')
            in_ = True
        item = obj(key.lower())
        if item and not kc_:
            if isinstance(value, str):
                value = value.lower()
            item = item.lower()
        if in_:
            if isinstance(value, str) and isinstance(item, str) and value not in item:
                return False
        elif item != value:
            return False
    return True
