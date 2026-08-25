# region 正常系
# サインアップテスト
def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )       
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# ログインテスト
def test_login(client):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )  
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
# endregion

# region 異常系
# サインアップ失敗(登録済みのメールアドレス)
def test_registrated_email(client):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )   
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    ) 
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registrated"
    
# ログイン失敗テスト(メールアドレス間違い)
def test_login_invalid_email(client):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )  
    response = client.post(
        "/auth/login",
        data={"username": "not_exist@example.com", "password": "password123"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"

# ログイン失敗テスト(パスワード間違い)
def test_login_wrong_password(client):
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )  
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpass"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"
# endregion