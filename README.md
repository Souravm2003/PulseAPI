# PulseAPI

PulseAPI is an API monitoring and analytics platform built to help developers keep track of their APIs and quickly understand when something goes wrong.

It periodically checks registered APIs, records their response status and response time, tracks failures and incidents, and displays the results through a web dashboard.

## What PulseAPI Does

With PulseAPI, users can:

- Register and log in securely
- Create and manage API monitors
- Configure the HTTP method, expected status code, timeout, and monitoring interval
- Automatically check APIs in the background
- Track API response times and status codes
- Monitor uptime and failure rates
- View P95 and P99 response times
- Track active and resolved incidents
- Receive email notifications when an API goes down or recovers
- View monitoring information through a web dashboard

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- PyJWT

### Database and Background Processing

- PostgreSQL
- Redis
- Celery
- Celery Beat

### Frontend

- HTML
- CSS
- JavaScript
- Django Templates

### Development Tools

- Git
- GitHub
- Docker
- Postman

## How It Works

The basic monitoring flow is:

```text
Django Dashboard
       |
       v
Django REST API
       |
       v
Monitor Configuration
       |
       v
Celery Beat
       |
       v
Celery Worker
       |
       v
API Request
       |
       v
Check Result
       |
       +------------------+
       |                  |
       v                  v
    Success            Failure
       |                  |
       v                  v
   Store Result      Track Failure
                          |
                          v
                    Create Incident
                          |
                          v
                     Send Email


