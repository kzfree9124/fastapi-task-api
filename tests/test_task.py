# トークンの取得
def get_token(client):    
    client.post(
        "/auth/signup",
        json = {"email": "user@example.com",
                "password": "password123"}
    )
    response = client.post(
        "/auth/login",
        data = {"username": "user@example.com",
                "password": "password123"}
    )
    return response.json()["access_token"]

# region 正常系
# タスク追加テスト
def test_create_task(client):
    token = get_token(client)
    
    response = client.post(
        "/tasks/",
        json = {"title": "Test Task",
               "description": "Test Desc"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Desc"

# タスク全件取得テスト
def test_get_tasks(client):
    token = get_token(client)
    
    client.post(
        "/tasks/",
        json = {"title": "Task1",
                "description": "Desc1"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task1"
    
# タスク更新テスト
def test_update_task(client):
    token = get_token(client)
    
    create_res = client.post(
        "/tasks/",
        json = {"title": "Old Title", "description": "Old Desc"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    task_id = create_res.json()["id"]
    
    update_res = client.put(
        f"/tasks/{task_id}",
        json = {"title": "New Title", "description": "New Desc"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["title"] == "New Title"
    assert data["description"] == "New Desc"
    
# タスク削除テスト
def test_delete_task(client):
    token = get_token(client)
    
    create_res = client.post(
        "/tasks/",
        json = {"title": "Task to delete", "description": "Desc"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    task_id = create_res.json()["id"]
    
    delete_res = client.delete(
        f"/tasks/{task_id}",
        headers = {"Authorization": f"Bearer {token}"}
    )
    
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Task deleted"
    
    get_res = client.get(
        "/tasks/",
        headers = {"Authorization": f"Bearer {token}"}
    )
    tasks = get_res.json()
    
    assert len(tasks) == 0
# endregion
    
# region 異常系
# タスク更新失敗テスト(存在しないユーザ)
def test_update_task_not_found(client):
    token = get_token(client)
    
    create_res = client.post(
        "/tasks/",
        json = {"title": "Task1", "description": "Desc1"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    existing_id = create_res.json()["id"]
    not_existing_id = existing_id + 1
    
    response = client.put(
        f"/tasks/{not_existing_id}",
        json = {"title": "New Title", "description": "New Desc"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
# タスク更新失敗テスト(他人のタスク)
def test_update_task_forbidden(client):
    # ユーザA作成
    client.post(
        "/auth/signup",
        json = {"email": "userA@example.com", "password": "passA"}
    )  
    loginA = client.post(
        "/auth/login", 
        data = {"username": "userA@example.com", "password": "passA"}
    )
    tokenA = loginA.json()["access_token"]
    
    # ユーザーAのタスク作成
    create_res = client.post(
        "/tasks/",
        json = {"title": "A Task", "description": "A Desc"},
        headers = {"Authorization": f"Bearer {tokenA}"}
    )
    task_id = create_res.json()["id"]
    
    # ユーザB作成
    client.post(
        "/auth/signup",
        json = {"email": "userB@example.com", "password": "passB"}
    )  
    loginB = client.post(
        "/auth/login", 
        data = {"username": "userB@example.com", "password": "passB"}
    )
    tokenB = loginB.json()["access_token"]
    
    # ユーザBがユーザAのタスクを更新
    response = client.put(
        f"/tasks/{task_id}",
        json = {"title": "Hack", "description": "Hack"},
        headers = {"Authorization": f"Bearer {tokenB}"}
    )
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"
    
# タスク削除失敗テスト(存在しないユーザ)
def test_delete_task_not_found(client):
    token = get_token(client)
    
    create_res = client.post(
        "/tasks/",
        json = {"title": "Task1", "description": "Desc1"},
        headers = {"Authorization": f"Bearer {token}"}
    )
    existing_id = create_res.json()["id"]
    not_existing_id = existing_id + 1
    
    response = client.delete(
        f"/tasks/{not_existing_id}",
        headers= {"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

# タスク削除失敗テスト(他人のタスク)
def test_delete_task_forbidden(client):
    # ユーザーA作成
    client.post(
        "/auth/signup",
        json = {"email": "userA@example.com", "password": "passA"}
    )
    loginA = client.post(
        "/auth/login", 
        data = {"username": "userA@example.com", "password": "passA"}
    )
    tokenA = loginA.json()["access_token"]

    # ユーザーAのタスク作成
    create_res = client.post(
        "/tasks/",
        json = {"title": "A Task", "description": "A Desc"},
        headers = {"Authorization": f"Bearer {tokenA}"}
    )
    task_id = create_res.json()["id"]

    # ユーザーB作成
    client.post(
        "/auth/signup",
        json = {"email": "userB@example.com", "password": "passB"}
    )
    loginB = client.post(
        "/auth/login", 
        data = {"username": "userB@example.com", "password": "passB"}
    )
    tokenB = loginB.json()["access_token"]

    # ユーザーBが A のタスクを削除しようとする → 403
    response = client.delete(
        f"/tasks/{task_id}",
        headers = {"Authorization": f"Bearer {tokenB}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

# endregion