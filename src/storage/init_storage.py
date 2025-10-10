from b2sdk.v2 import *

from app import settings
from app.log import  log

def init_remote_storage() -> B2Api | dict:
    if is_backblaze():
        config = settings.STORAGE_CONFIG['backblaze']
        info = InMemoryAccountInfo()
        b2_api = B2Api(info, cache=AuthInfoCache(info))
        application_key_id = config['application_key_id']
        application_key = config['application_key']
        b2_api.authorize_account("production", application_key_id, application_key)
        return b2_api
    if is_bunny():
        config = settings.STORAGE_CONFIG.get('bunny')
        access_key = config.get('storage_api_key')
        storage_zone_name = config.get('storage_zone_name')
        base_url = config.get('base_url')
        base_url = f"{base_url}/{storage_zone_name}"
        return {
            'access_key': access_key,
            'base_url': base_url,
            'storage_zone_name': storage_zone_name
        }

    raise Exception('Storage provider is not defined')


def is_backblaze():
    return settings.STORAGE_TYPE == 'backblaze'


def is_bunny():
    return settings.STORAGE_TYPE == 'bunny'
