# Slidespeak Coding Challenge 2025

This project consists of three main services: `unoserver`, `backend`, and `frontend`.

---

## Prerequisites

Before running the project, you need to set up environment files for the backend and frontend services.

### Environment Files Setup

1. **Backend Environment File**

   - Create a file named `.env` in the `./backend/` directory
   - Add the following environment variables:

   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
   AWS_S3_BUCKET=your_s3_bucket_name
   AWS_REGION=your_aws_region
   UNOSERVER_URL=http://unoserver:2004
   FRONTEND_URL=http://localhost:3000
   BACKEND_URL=http://localhost:8000
   ```

2. **Frontend Environment File**
   - Create a file named `.env` in the `./frontend/` directory
   - Add the following environment variables:
   ```
   UNOSERVER_URL=http://unoserver:2004
   FRONTEND_URL=http://localhost:3000
   BACKEND_URL=http://localhost:8000
   ```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
```

### 2. Build and start the services

```bash
docker-compose up --build
```

### 3. Access the services:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000 (optional)
- UnoServer: http://localhost:2004 (optional)

### 4. To stop the services:

```bash
docker-compose down
```