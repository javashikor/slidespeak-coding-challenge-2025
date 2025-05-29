# Slidespeak Coding Challenge 2025

This project consists of five main services: `backend`, `frontend`, `redis`, `celery_worker`, and `unoserver`.

---

## Prerequisites

Before running the project, you need to set up environment files for the backend service.

### Environment Files Setup

1. **Backend Environment File**
   - Create a file named `.env` in the root directory of the project
   - Add the following environment variables:
   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
   AWS_S3_BUCKET=your_s3_bucket_name
   AWS_REGION=your_aws_region
   UNOSERVER_URL=http://unoserver:2004
   FRONTEND_URL=http://localhost:3000
   BACKEND_URL=http://localhost:8000
   REDIS_URL=redis://redis:6379/0
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/javashikor/slidespeak-coding-challenge-2025.git
cd slidespeak-coding-challenge-2025
```

### 2. Create Environment File
Create a `.env` file in the root directory with the required environment variables (see Prerequisites section above).

### 3. Build and Start the Services
```bash
docker-compose up --build
```

### 4. Access the Services:
- **Frontend**: http://localhost:3000 (Main application interface)
- **Backend API**: http://localhost:8000 (API documentation available at `/docs`)
- **Redis**: http://localhost:6379 (Database for task queue and results)
- **UnoServer**: http://localhost:2004 (Document conversion service)

### 5. To Stop the Services:
```bash
docker-compose down
```

---

## How It Works

1. **File Upload**: Users drag and drop PPTX files through the frontend interface
2. **Task Creation**: The backend creates a Celery task for background processing
3. **Conversion**: The Celery worker processes the file using UnoServer (LibreOffice)
4. **Storage**: Converted PDF is uploaded to AWS S3
5. **Results**: Task results and download URLs are stored in Redis
6. **Download**: Users can download the converted PDF from S3

---

## File Type Support

This application currently supports:
- **Input**: PowerPoint files (`.pptx` only)
- **Output**: PDF files
