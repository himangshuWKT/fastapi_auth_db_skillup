from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
from app.auth import create_access_token
from app.models import User

client = TestClient(app)

def test_read_items():
    user = User(id=1, username="testuser")
    token = create_access_token(data={"sub": user.id})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/items", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"name": "Item 1"}, {"name": "Item 2"}]

# ... more tests