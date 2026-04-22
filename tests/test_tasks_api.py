import requests

def test_create_task_returns_201_and_created_task(base_url,wait_for_api):

    payload = {
        "title": "Train",
        "description": "Muay Thai at 19:00",
        "task_date": "2026-04-22",
        "status": "new",
    }

    r = requests.post(f'{base_url}/tasks', json=payload, timeout=10)

    assert r.status_code == 201

    b = r.json()

    assert b['id']
    assert b['title'] == payload['title']
    assert b['description'] == payload['description']
    assert b['task_date'] == payload['task_date']
    assert b['status'] == payload['status']
    assert b['created_at']

def test_create_task_with_empty_title_returns_422(base_url,wait_for_api):

    payload = {
        "title": "",
        "description": "Muay Thai at 19:00",
        "task_date": "2026-04-22",
        "status": "new",
    }

    r = requests.post(f'{base_url}/tasks', json=payload, timeout=10)

    assert r.status_code == 422

def test_create_task_without_required_task_date_returns_422(base_url,wait_for_api):

    payload = {
        "title": "Train",
        "description": "Muay Thai at 19:00",
        "task_date": "",
        "status": "new",
    }

    r = requests.post(f'{base_url}/tasks', json=payload, timeout=10)

    assert r.status_code == 422

def test_create_task_with_invalid_status_returns_422(base_url,wait_for_api):

    payload = {
        "title": "Train",
        "description": "Muay Thai at 19:00",
        "task_date": "2026-04-22",
        "status": "invalid",
    }

    r = requests.post(f'{base_url}/tasks', json=payload, timeout=10)

    assert r.status_code == 422

def test_create_task_without_description_returns_201(base_url,wait_for_api):

    payload = {
        "title": "Train",
        "task_date": "2026-04-22",
        "status": "new",
    }

    r = requests.post(f'{base_url}/tasks', json=payload, timeout=10)

    assert r.status_code == 201

def test_get_task_by_id_returns_200_and_task(base_url,wait_for_api):

    payload = {
        "title": "Read book",
        "description": "30 pages",
        "task_date": "2026-04-22",
        "status": "new",
    }

    r_create = requests.post(f'{base_url}/tasks', json=payload, timeout=10)
    task_id = r_create.json()['id']

    r_get = requests.get(f'{base_url}/tasks/{task_id}', timeout=10)

    assert r_get.status_code == 200

    b = r_get.json()

    assert b['id'] == task_id
    assert b['title'] == payload['title']

def test_get_task_by_id_for_nonexistent_task_returns_404(base_url,wait_for_api):

    r = requests.get(f'{base_url}/tasks/99999999', timeout = 10)

    assert r.status_code == 404

    b = r.json()

    assert b == {"detail": "Task not found"}

def test_get_task_by_id_with_invalid_id_type_returns_422(base_url,wait_for_api):

    r = requests.get(f'{base_url}/tasks/abc', timeout = 10)

    assert r.status_code == 422

def test_get_tasks_by_date_returns_tasks_only_for_requested_day(base_url,wait_for_api):

    first_task = {
        "title": "Task 1",
        "description": "desc 1",
        "task_date": "2026-04-22",
        "status": "new",
    }
    second_task = {
        "title": "Task 2",
        "description": "desc 2",
        "task_date": "2026-04-22",
        "status": "done",
    }
    third_task = {
        "title": "Task 3",
        "description": "desc 3",
        "task_date": "2026-04-23",
        "status": "new",
    }

    requests.post(f"{base_url}/tasks", json=first_task, timeout=5)
    requests.post(f"{base_url}/tasks", json=second_task, timeout=5)
    requests.post(f"{base_url}/tasks", json=third_task, timeout=5)

    r = requests.get(f"{base_url}/tasks", params={"date": "2026-04-22"}, timeout=5)

    assert r.status_code == 200
    b = r.json()

    returned_titles = {item['title'] for item in b}

    assert first_task['title'] in returned_titles
    assert second_task['title'] in returned_titles
    assert third_task['title'] not in returned_titles


def test_get_tasks_by_date_returns_empty_list_when_no_tasks_exist_for_day(base_url,wait_for_api):

    r = requests.get(f"{base_url}/tasks", params={"date": "2999-04-22"}, timeout=5)

    assert r.status_code == 200
    b = r.json()

    assert b == []

def test_get_tasks_by_date_with_invalid_date_format_returns_422(base_url,wait_for_api):

    r = requests.get(f"{base_url}/tasks", params={"date": "not a date"}, timeout=5)

    assert r.status_code == 422

def test_get_tasks_by_date_without_query_param_returns_422(base_url,wait_for_api):

    r = requests.get(f"{base_url}/tasks", timeout=5)

    assert r.status_code == 422

def test_patch_task_updates_only_sent_fields(wait_for_api, base_url):
    create_payload = {
        "title": "Old title",
        "description": "Old description",
        "task_date": "2026-04-22",
        "status": "new",
    }

    create_response = requests.post(f"{base_url}/tasks", json=create_payload, timeout=5)
    task_id = create_response.json()["id"]

    patch_payload = {"status": "done"}

    response = requests.patch(f"{base_url}/tasks/{task_id}", json=patch_payload, timeout=5)

    assert response.status_code == 200
    body = response.json()

    assert body["title"] == "Old title"
    assert body["description"] == "Old description"
    assert body["status"] == "done"

def test_delete_task_returns_204_and_task_becomes_unavailable(wait_for_api, base_url):
    create_payload = {
        "title": "Delete me",
        "description": "temporary task",
        "task_date": "2026-04-22",
        "status": "new",
    }

    create_response = requests.post(f"{base_url}/tasks", json=create_payload, timeout=5)
    task_id = create_response.json()["id"]

    delete_response = requests.delete(f"{base_url}/tasks/{task_id}", timeout=5)
    assert delete_response.status_code == 204

    get_response = requests.get(f"{base_url}/tasks/{task_id}", timeout=5)
    assert get_response.status_code == 404