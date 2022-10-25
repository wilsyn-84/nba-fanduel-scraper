import requests

def make_request(url, params):
    return requests.get(url, params=_assemble_query_params(params))


def _assemble_query_params(params):
    return {key: value for key, value in params}