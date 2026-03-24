# Azure FastAPI DevOps Project
A production-style cloud project that deploys a containerized FastAPI application to Azure using Terraform, Azure Container Apps, Managed Identity, Key Vault, Blob Storage, and GitHub Actions CI/CD.

# OVERVIEW
This project demonstrates how to build, secure, and deploy a cloud-native application without hardcoding credentials.

It includes:

A FastAPI backend

Docker containerization

Infrastructure as Code (Terraform)

Secure secret management via Azure Key Vault

Managed Identity authentication (no secrets in code)

Azure Blob Storage integration

GitHub Actions CI/CD pipeline

# ARCHITECTURE
<img width="3760" height="1271" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/4e840f7c-bee1-47f2-b230-599d48b47b99" />

# TECH STACK
Python / FastAPI

Docker

Terraform

Azure Container Apps

Azure Container Registry (ACR)

Azure Key Vault

Azure Blob Storage

Managed Identity (RBAC)

GitHub Actions (CI/CD)

# SECURITY DESIGN
No credentials stored in code

Managed Identity used for Azure authentication

Secrets retrieved dynamically from Key Vault

Storage access controlled via RBAC

Write endpoint protected by API key

# API ENDPOINTS
<img width="1429" height="434" alt="Screenshot 2026-03-24 at 5 11 20 PM" src="https://github.com/user-attachments/assets/2af005a7-a6e2-40cc-a64a-3b12e50a5c6c" />

# AUTHENTICATION
Protected endpoints require header: x-api-key: dev-secret-key

# CI/CD PIPELINE
GitHub Actions automatically:

1. Builds Docker image
2. Pushes image to Azure Container Registry
3. Updates Azure Container App with new image

Trigger: git push to main

# TESTING
Basic tests included using pytest: pytest ./app
Covers: root endpoint, health check, unauthorized access

# INFRASTRUCTURE (TERRAFORM)
Resources managed via Terraform: Container App, Container App Environment, Log Analytics Workspace
Example: terraform init, terraform apply

# STORAGE FLOW
1. App retrieves storage account name from Key Vault
2. Uses Managed Identity to authenticate
3. Writes blob to container appdata

# COST OPTIMIZATION
Container Apps configured with: min_replicas = 0 (Scales to zero when idle)

# CLEANUP
To avoid charges, delete: Container App, Container App Environment, Log Analytics Workspace

Keep only if needed: ACR, Key Vault, Storage Account

# KEY LEARNINGS
Managed Identity vs secrets-based auth

Terraform vs manual Azure drift issues

RBAC propagation delays

ACR authentication setup

ARM vs AMD64 Docker image issues

Key Vault naming constraints

# HOW TO RUN LOCALLY
cd app

pip install -r requirements.txt

uvicorn main:app --reload

# BUILD & PUSH IMAGE
docker buildx build --platform linux/amd64 \

  -t <acr-name>.azurecr.io/p16-fastapi:<tag> \
  
  --push .

# SCREENSHOTS
<img width="655" height="145" alt="Screenshot 2026-03-24 at 5 07 00 PM" src="https://github.com/user-attachments/assets/fb27275d-f215-4f57-9dd9-b25dbf325dcd" />

Application Demo

<img width="655" height="145" alt="Screenshot 2026-03-24 at 5 07 16 PM" src="https://github.com/user-attachments/assets/04006828-314f-486b-b1f5-a607b320ef33" />

Secure secret retrieval from Azure Key Vault without hardcoded credentials

<img width="1411" height="764" alt="Screenshot 2026-03-24 at 5 09 09 PM" src="https://github.com/user-attachments/assets/999763d9-009d-4cb6-bce3-00036d2d7ccb" />

Successful write to Azure Blob Storage using Managed Identity authentication

# AUTHOR
Built as part of a hands-on DevOps/cloud engineering learning journey.
