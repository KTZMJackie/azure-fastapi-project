from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_write_unauthorized():
    response = client.post("/write")
    assert response.status_code == 401


def test_secret_missing_env_var():
    """GET /secret returns 500 when KEY_VAULT_NAME is not set."""
    with patch.dict("os.environ", {}, clear=True):
        import os
        os.environ.pop("KEY_VAULT_NAME", None)
        response = client.get("/secret")
    assert response.status_code == 500
    assert "KEY_VAULT_NAME" in response.json()["detail"]


def test_write_with_valid_key_mocked():
    """POST /write succeeds with valid API key when Azure is mocked."""
    mock_blob_client = MagicMock()
    mock_blob_client.upload_blob.return_value = None

    mock_bsc = MagicMock()
    mock_bsc.get_blob_client.return_value = mock_blob_client

    with patch("main._get_blob_service_client", return_value=mock_bsc):
        response = client.post(
            "/write",
            headers={"x-api-key": "dev-secret-key"}
        )

    assert response.status_code == 200
    assert "blob_name" in response.json()


def test_read_blob_not_found_mocked():
    """GET /read returns 404 when blob does not exist."""
    mock_blob_client = MagicMock()
    mock_blob_client.download_blob.side_effect = Exception("BlobNotFound")

    mock_bsc = MagicMock()
    mock_bsc.get_blob_client.return_value = mock_blob_client

    with patch("main._get_blob_service_client", return_value=mock_bsc):
        response = client.get("/read?blob_name=nonexistent.txt")

    assert response.status_code == 404
    assert "Blob not found" in response.json()["detail"]


def test_read_success_mocked():
    """GET /read returns content when blob exists."""
    mock_blob_client = MagicMock()
    mock_blob_client.download_blob.return_value.readall.return_value = b"Hello from Managed Identity + Key Vault"

    mock_bsc = MagicMock()
    mock_bsc.get_blob_client.return_value = mock_blob_client

    with patch("main._get_blob_service_client", return_value=mock_bsc):
        response = client.get("/read?blob_name=test-blob.txt")

    assert response.status_code == 200
    assert response.json()["content"] == "Hello from Managed Identity + Key Vault"
    assert response.json()["blob_name"] == "test-blob.txt"
