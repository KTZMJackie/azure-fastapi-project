import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Header
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

app = FastAPI()

CONTAINER_NAME = "appdata"
SECRET_NAME = "storage-account-name"
API_KEY = os.getenv("API_KEY", "dev-secret-key")


def verify_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Hello from FastAPI on Azure Container Apps - CI/CD live"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/secret")
def secret():
    kv_name = os.environ.get("KEY_VAULT_NAME")
    if not kv_name:
        raise HTTPException(status_code=500, detail="Missing env var KEY_VAULT_NAME")

    secret_name = os.environ.get("KEY_VAULT_SECRET_NAME", "HELLO_SECRET")
    kv_url = f"https://{kv_name}.vault.azure.net/"

    client = SecretClient(vault_url=kv_url, credential=DefaultAzureCredential())
    _ = client.get_secret(secret_name)

    return {"secret_name": secret_name, "retrieved": True}


def _get_blob_service_client():
    key_vault_name = os.getenv("KEY_VAULT_NAME")
    if not key_vault_name:
        raise HTTPException(status_code=500, detail="Missing env var KEY_VAULT_NAME")

    credential = DefaultAzureCredential()

    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    secret_client = SecretClient(vault_url=kv_uri, credential=credential)

    storage_account_name = secret_client.get_secret(SECRET_NAME).value
    account_url = f"https://{storage_account_name}.blob.core.windows.net"

    return BlobServiceClient(account_url=account_url, credential=credential)


@app.post("/write")
def write(x_api_key: str | None = Header(default=None)):
    verify_api_key(x_api_key)

    bsc = _get_blob_service_client()
    blob_name = f"{uuid4()}.txt"
    blob_client = bsc.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    blob_client.upload_blob("Hello from Managed Identity + Key Vault", overwrite=True)

    return {"blob_name": blob_name}


@app.get("/read")
def read(blob_name: str):
    bsc = _get_blob_service_client()
    blob_client = bsc.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

    try:
        data = blob_client.download_blob().readall().decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Blob not found or cannot read: {e}")

    return {"blob_name": blob_name, "content": data}