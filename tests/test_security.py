from jose import jwt
import time
from app.core.config import settings

# --------------正常系--------------
# test_task.pyで実施するため省略

# --------------異常系--------------
# トークンにユーザID(sub)が含まれていない場合
def test_no_sub(client):    
    token= jwt.encode(
        {"foo": "bar"},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
    
# 期限切れの場合
def test_expired_token(client):
    expired_payload = {
        "sub": "1",
        "exp": int(time.time()) - 10
    }
    
    token = jwt.encode(
        expired_payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"
    
# 不正な文字列の場合
def test_invalid_token(client):
    invalid_token = "this.is.not.jwt"
    
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer " + invalid_token}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
    
# トークンは有効だが、DBにユーザがいない場合
def test_user_not_found(client):
    client.post(
        "/auth/signup",
        json = {"email": "user@example.com",
                "password": "password123"}
    )
    client.post(
        "/auth/login",
        json = {"email": "user@example.com",
                "password": "password123"}
    )
    
    token = jwt.encode(
        {"sub": "9999"},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"