# FastAPI Trade API

## Project Overview

This project is a FastAPI-based web service that handles trade order management. It includes endpoints to place trade orders, retrieve trade order history, and provides real-time order updates via WebSockets. The application is containerized using Docker, deployed to an AWS EC2 instance, and uses a self-hosted GitHub Actions runner for continuous integration and continuous deployment (CI/CD).

---

## Features

- REST API built with FastAPI
- Real-time order updates using WebSockets
- Containerized using Docker for consistent deployment
- Deployed on AWS EC2 using Docker
- CI/CD pipeline using a self-hosted GitHub Actions runner on the AWS EC2 instance

---

## Technologies Used

- **FastAPI** - Web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Docker** - Containerization platform
- **AWS EC2** - Cloud service to host the application
- **GitHub Actions** - CI/CD tool for automated deployments
- **SQLite** (local development) and **PostgreSQL** (production)

---

## Prerequisites

- Python 3.11+
- Docker
- AWS account and an EC2 instance
- SSH key pair for the EC2 instance
- GitHub repository for code management

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Dhrumit26/fastapi-trade-api.git
cd fastapi-trade-api
```

### 2. Install Dependencies

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Application Locally

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Open the browser and visit: `http://localhost:8000/docs` to interact with the API documentation.

---

## Dockerization

### Build the Docker Image

```bash
docker build -t fastapi-trade-api .
```

### Run the Docker Container

```bash
docker run -d -p 80:8000 fastapi-trade-api
```

---

## Deploying to AWS EC2

1. Launch an Ubuntu EC2 instance with security group rules to allow inbound traffic on port 80 and port 22 (SSH).
2. SSH into the instance using your key:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

3. Install Docker on the EC2 instance:
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. Transfer the project to the EC2 instance:
   ```bash
   scp -i your-key.pem -r /path/to/fastapi-trade-api ubuntu@your-ec2-public-ip:/home/ubuntu/
   ```

5. Build and run the Docker container on the EC2 instance:
   ```bash
   cd fastapi-trade-api
   sudo docker build -t fastapi-trade-api .
   sudo docker run -d -p 80:8000 fastapi-trade-api
   ```

---

## Setting Up Self-Hosted GitHub Actions Runner

1. SSH into your EC2 instance and set up the runner:
   ```bash
   mkdir actions-runner && cd actions-runner
   curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.308.0/actions-runner-linux-x64-2.308.0.tar.gz
   tar xzf actions-runner-linux-x64.tar.gz
   ./config.sh --url https://github.com/Dhrumit26/fastapi-trade-api --token YOUR_TOKEN
   ```

2. Start the runner:
   ```bash
   ./run.sh
   ```

3. Install the runner as a service:
   ```bash
   sudo ./svc.sh install
   sudo ./svc.sh start
   ```

---

## CI/CD Pipeline Configuration

The CI/CD pipeline is defined in the `.github/workflows/deploy.yml` file:

```yaml
name: FastAPI CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: self-hosted
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build and Deploy Docker Image
        run: |
          sudo docker stop $(sudo docker ps -aq) || true
          sudo docker rm $(sudo docker ps -aq) || true
          sudo docker build -t fastapi-trade-api .
          sudo docker run -d -p 80:8000 fastapi-trade-api
```

---

## API Endpoints

- **POST /orders**: Place a new trade order.
- **GET /orders**: Retrieve all trade orders.
- **WebSocket /ws**: Real-time order updates.

---

## Accessing the Application

The application is accessible via the public IP address of the EC2 instance:

```bash
http://your-ec2-public-ip
```

---

## Troubleshooting

- **Container Issues**: Check running containers using `docker ps`.
- **Logs**: View container logs using `docker logs <container_id>`.
- **CI/CD Failures**: Review GitHub Actions logs for details on pipeline failures.

---

