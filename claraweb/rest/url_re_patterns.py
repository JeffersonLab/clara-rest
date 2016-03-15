# coding=utf-8


class URLPattern:

    DPE_URL = r'^(?P<DPE_id>[a-z0-9]+)'
    CONTAINER_URL = r'^(?P<container_id>[a-z0-9]+)'
    SERVICE_URL = r'^(?P<service_id>[a-z0-9]+)/?$'
