import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def wait_for_api(base_url):
    for _ in range(30):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass

    raise RuntimeError("API is not available at http://127.0.0.1:8000")