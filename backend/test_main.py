from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

test_email = "testrunner@example.com"
test_password = "securepassword"

# 1. Signup Test
def test_1_signup():
    response = client.post(
        "/signup",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code in [200, 400]

# 2. Login Test (Aur Token lana)
@pytest.fixture
def get_token():
    # Ye function test nahi hai, ye helper hai jo token layega
    response = client.post(
        "/login",
        data={"username": test_email, "password": test_password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# 3. Create Task (Token fixture use karega)
def test_3_create_task(get_token):
    token = get_token # Upar wale function se token apne aap aa gaya
    
    response = client.post(
        "/tasks",
        json={"title": "Automated Test Task", "is_completed": False},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Automated Test Task"

# 4. Read Tasks
def test_4_read_tasks(get_token):
    token = get_token
    
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

# 5. Security Check
def test_5_security_check():
    response = client.get("/tasks")
    assert response.status_code == 401

# --- UPDATE TASK ---
def test_6_update_task(get_token):
    token = get_token
    
    # Step A: Pehle ek naya task banao
    create_res = client.post(
        "/tasks",
        json={"title": "Task to Update", "is_completed": False},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_res.json()["id"] # ID nikali
    
    # Step B: Ab us ID par PUT request bhejo (Status True karo)
    update_res = client.put(
        f"/tasks/{task_id}",
        json={"title": "Task to Update", "is_completed": True}, # True bheja
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Step C: Assertions
    assert update_res.status_code == 200
    assert update_res.json()["is_completed"] == True # Check kiya ki True hua ya nahi
    assert update_res.json()["id"] == task_id