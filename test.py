
import io
from fastapi.testclient import TestClient
from main import app
import ml.caption_model as caption_model

client = TestClient(app)

def test_prediction(monkeypatch):
    # Mock caption generator instead of real ML model
    def mock_caption(path): return "Mocked herbal plant caption"
    monkeypatch.setattr(caption_model, "generate_caption", mock_caption)

    # Register a user first (needed for prediction)
    user = {"username": "testuser", "email": "test@example.com", "password": "secret"}
    resp = client.post("/user/register", json=user)
    assert resp.status_code == 200
    user_id = resp.json()["id"]

    # Upload fake image
    fake_img = io.BytesIO(b"fake image data")
    files = {"file": ("plant.jpg", fake_img, "image/jpeg")}
    pred_resp = client.post(f"/user/prediction?user_id={user_id}", files=files)

    # Check prediction response
    assert pred_resp.status_code == 200
    data = pred_resp.json()
    assert data["caption"] == "Mocked herbal plant caption"
    assert data["user_id"] == user_id
    assert "plant.jpg" in data["image_path"]