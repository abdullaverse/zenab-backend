# Deployment Guide for ZENAB IoT Backend

This guide explains how to deploy your Python Flask backend (`zenab-backend`) to the cloud so it's accessible from anywhere.

## 1. Local Preparation
Before deploying, ensure your backend project has the necessary files:
- **app.py**: The main Flask application.
- **dashboard.html**: The UI served at the root.
- **requirements.txt**: List of dependencies (Flask, flask-cors, gunicorn).
- **telemetry_history.json**: Your data storage (Note: Cloud platforms may reset this file on restart).

## 2. Deploying to Render.com (Recommended)
[Render](https://render.com) is a great free service for hosting Python apps.

1.  **Push to GitHub**: If you haven't already, push your `zenab-backend` folder to a GitHub repository.
2.  **Create a New Web Service**:
    - Sign in to Render.com.
    - Click **New** > **Web Service**.
    - Connect your GitHub repository.
3.  **Configure the Service**:
    - **Language**: `Python`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app` (This uses gunicorn as a production-grade server).
4.  **Wait for Deployment**: Render will build and deploy your app. Once finished, you'll get a URL like `https://zenab-backend-xxxx.onrender.com`.

## 3. Important Notes for Cloud Hosting
> [!WARNING]
> **Data Persistence**: Most free cloud hosting services (like Render's free tier) use "ephemeral storage". This means `telemetry_history.json` will be wiped and reset to the version in your GitHub repo every time the server restarts.
> 
> To keep data permanently, you should eventually migrate to a database like **Supabase (PostgreSQL)** or **MongoDB Atlas**.

## 4. Update the Frontend
Once your backend is live:
1.  Copy your new backend URL.
2.  In your ZENAB IDE (frontend), locate where the API URL is defined (usually in `app.js`).
3.  Update the URL to your new cloud endpoint:
    ```javascript
    const apiUrl = "https://your-backend-url.onrender.com/api/data";
    ```
4.  Deploy your frontend (e.g., to GitHub Pages) to complete the cloud setup.
