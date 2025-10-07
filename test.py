import os
from fastapi.testclient import TestClient
from main import app   # <-- make sure main.py creates FastAPI app = FastAPI()

client = TestClient(app)

def test_create_prediction():
    # Mock user_id (this must exist in your DB for the test to pass)
    user_id = "65123abc456def7890"  

    # Use a sample test image
    test_image_path = "tests/sample_plant.jpg"  # make sure you have this file

    # Open image in binary mode and send as multipart/form-data
    with open(test_image_path, "rb") as img:
        response = client.post(
            f"/user/prediction?user_id={user_id}",
            files={"file": ("sample_plant.jpg", img, "image/jpeg")},
        )

    # Check response
    assert response.status_code == 200, response.text
    data = response.json()

    # Print output for debugging
    print(data)

    # Validate fields exist in response
    assert "caption" in data
    assert "plant_name" in data
    assert "scientific_name" in data
    assert "confidence" in data
    assert "image_path" in data
    assert "created_at" in data
