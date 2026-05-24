import requests
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2


MAPBOX_BASE = "https://api.mapbox.com/geocoding/v5/mapbox.places"


def geocode_address(address: str, country: str = 'KE', proximity: str = None) -> dict | None:
    """
    address   → string to geocode
    country   → ISO 3166-1 alpha-2 code. Default 'KE' (Kenya)
                pass None to search globally
    proximity → 'lng,lat' string to bias toward a point
    """
    url = f"{MAPBOX_BASE}/{requests.utils.quote(address)}.json"

    params = {
        'access_token': settings.MAPBOX_ACCESS_TOKEN,
        'limit': 1,
        'types': 'place,address,locality,neighborhood',
        'country': country,  # ← this is the fix
    }

    if proximity:
        params['proximity'] = proximity  # e.g. '36.8219,-1.2921' (Nairobi CBD)

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get('features'):
        return None

    feature = data['features'][0]
    lng, lat = feature['geometry']['coordinates']

    return {
        'lat': lat,
        'lng': lng,
        'place_name': feature['place_name']
    }

def reverse_geocode(lat: float, lng: float) -> str | None:
    """
    Coordinates → address string
    Returns: 'Westlands, Nairobi, Kenya'
    """
    url = f"{MAPBOX_BASE}/{lng},{lat}.json"  # Mapbox wants lng,lat order

    response = requests.get(url, params={
        'access_token': settings.MAPBOX_ACCESS_TOKEN,
        'limit': 1
    })

    data = response.json()

    if not data.get('features'):
        return None

    return data['features'][0]['place_name']


def calculate_distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Haversine formula — straight line distance between two coordinates.
    Returns distance in kilometers.
    No API call needed — pure math.
    """
    R = 6371  # Earth radius in km

    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return round(R * c, 2)


def find_nearby_users(origin_lat: float, origin_lng: float, radius_km: float, profiles):
    """
    Filter a queryset of UserProfiles to those within radius_km.
    profiles = UserProfile.objects.exclude(lat=None)
    """
    nearby = []
    for profile in profiles:
        if profile.lat is None or profile.lng is None:
            continue

        distance = calculate_distance_km(
            origin_lat, origin_lng,
            profile.lat, profile.lng
        )

        if distance <= radius_km:
            nearby.append({
                'user_id': profile.user.id,
                'username': profile.user.username,
                'place_name': profile.place_name,
                'distance_km': distance
            })

    # sort closest first
    return sorted(nearby, key=lambda x: x['distance_km'])