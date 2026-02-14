import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app, db
from app.models import User


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_CONFIG"] = "testing"
    application = create_app("testing")
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_token(app, client):
    with app.app_context():
        u = User.query.filter_by(username="admin").first()
        if u is None:
            u = User(username="admin", email="admin@test.com", is_admin=True, is_active=True)
            db.session.add(u)
        u.set_password("admin123")
        u.is_admin = True
        u.is_active = True
        db.session.commit()
    r = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    data = r.get_json()
    return data["data"]["token"]
