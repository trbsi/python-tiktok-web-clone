import geoip2.database

from app import settings


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_ip_data(ip: str | None = None):
    """
    Detects timezone based on IP address using ipinfo.io API.
    If no IP is provided, it will auto-detect your current public IP.
    """
    data = {
        'timezone': None,
        'country': None,
        'state': None,
    }
    if not ip:
        return data

    try:
        reader = geoip2.database.Reader(settings.IP_DATABASE_PATH)
        response = reader.city(ip)
        data = {
            'timezone': response.location.time_zone,
            'country': response.country.iso_code,
            'state': response.subdivisions.most_specific.iso_code
        }
        reader.close()

        return data
    except Exception as e:
        return data
