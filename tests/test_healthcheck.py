import requests

def test_healthcheck_returns_200(base_url,wait_for_api):
    r= requests.get(f'{base_url}/health', timeout = 10)
    assert r.status_code == 200
    assert r.json() == {'status':'ok'}
