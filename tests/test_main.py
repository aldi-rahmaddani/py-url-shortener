from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app.config.db import get_db
from app.models.user import User
from app.models.url import URL

client = TestClient(app)

TEST_USER = {
  "name": "Test User",
  "email": "testuser@gmail.com",
  "password": "testpassword123"
}

TEST_URL = {
    "original_url": "https://example.com"
}

# root
def test_get_welcome():
  response = client.get("/")
  assert response.status_code==200
  assert 'message' in response.json() 

# register
def test_register_user():
  """Test endpoint /register untuk mendaftarkan user baru."""
  response = client.post("/auth/register", json=TEST_USER)
  assert response.status_code == 200
  assert response.json()["message"] == "Registration successful"

# login
def test_login_user():
  """Test endpoint /login untuk mendapatkan access_token."""
  response = client.post("/auth/login", data={
        "username": TEST_USER["email"], 
        "password": TEST_USER["password"]
    })

  assert response.status_code == 200
  assert "access_token" in response.json()

  # Simpan token untuk test berikutnya
  global access_token
  access_token = response.json()["access_token"]

def test_create_short_url():
    """Test membuat URL pendek dengan token autentikasi."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.post("/short", json=TEST_URL, headers=headers)
    assert response.status_code == 200
    assert "short_url" in response.json()
    global short_url
    short_url = response.json()["short_url"]  # Simpan URL pendek untuk test lain

def test_get_user_urls():
    """Test mengambil semua URL yang dibuat oleh user yang login."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/short/list", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Pastikan respons adalah list

# clean up
def test_cleanup_url():
  """Hapus short url test dari database setelah pengujian selesai."""
  db: Session = next(get_db())  # Dapatkan sesi database
  url = db.query(URL).filter(URL.short_url == short_url).first()

  if url:
    db.delete(url)
    db.commit()
  
  db.close()

def test_cleanup_user():
  """Hapus user test dari database setelah pengujian selesai."""
  db: Session = next(get_db())  # Dapatkan sesi database
  user = db.query(User).filter(User.email == TEST_USER["email"]).first()
    
  if user:
    db.delete(user)  # Hapus user dari database
    db.commit()
    
  db.close()