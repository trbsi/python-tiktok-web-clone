import requests


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_timezone_from_ip(ip: str | None = None):
    """
    Detects timezone based on IP address using ipinfo.io API.
    If no IP is provided, it will auto-detect your current public IP.
    """
    url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
    try:
        response = requests.get(url)
        data = response.json()
        timezone = data.get("timezone")
        return timezone
    except Exception as e:
        return None
