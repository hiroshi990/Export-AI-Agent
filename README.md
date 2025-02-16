# Export Assistance AI Agent

Export Assistance AI is an intelligent assistant designed to help businesses and exporters navigate the complexities of exporting goods to the **USA & Europe**. This AI-powered platform provides recommendations on **suitable products for export**, **regulatory compliance insights**, and **market strategies** to optimize international trade. 

## Features

- **AI-Powered Recommendations**: Suggests the best products for export to the USA and Europe.
- **Export Compliance Guidance**: Provides insights on regulations, compliance, and legal requirements.
- **Market Strategy Optimization**: Helps businesses develop marketing strategies for effective trade.
- **Supplier & Logistics Support**: Assists in establishing relationships with suppliers and logistics providers.
- **Interactive Chat Interface**: Enables users to ask questions about export procedures, compliance, and strategies.

## Technologies Used

- **Streamlit**: Used for creating the interactive web interface.
- **Docker**: Enables easy deployment and containerization.

## Prerequisites

Ensure you have the following installed before proceeding:

- [Docker](https://www.docker.com/get-started) (for running the app in a container)
- [Python 3.8+](https://www.python.org/downloads/) (if running locally)
- Dependencies listed in `requirements.txt`

## Installation & Setup
### Running Locally (Without Docker)
If you prefer to run the project on your local machine without Docker, follow these steps:
1. Clone the repository:
   
   ```bash
   git clone https://github.com/hiroshi990/Export-AI-Agent.git
   cd Export-AI-Agent
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
3. Run the application:

   ```bash
   streamlit run app.py

### Running with Docker (Recommended)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hiroshi990/Export-AI-Agent.git
   cd Export-AI-Agent
2. **You can use the docker image using the Dockerfile**:
   ```bash
    # Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7
    
    ARG PYTHON_VERSION=3.12.4
    FROM python:${PYTHON_VERSION} as base
    
    # Prevents Python from writing pyc files.
    ENV PYTHONDONTWRITEBYTECODE=1
    
    # Keeps Python from buffering stdout and stderr to avoid situations where
    # the application crashes without emitting any logs due to buffering.
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Create a non-privileged user that the app will run under.
    ARG UID=10001
    RUN adduser \
        --disabled-password \
        --gecos "" \
        --home "/nonexistent" \
        --shell "/sbin/nologin" \
        --no-create-home \
        --uid "${UID}" \
        appuser
    
    # Create a writable cache directory for the non-privileged user
    RUN mkdir -p /home/appuser/.cache && chown -R appuser:appuser /home/appuser/.cache
    
    # Set the TRANSFORMERS_CACHE environment variable to the writable cache directory
    ENV TRANSFORMERS_CACHE=/home/appuser/.cache
    
    
    # Download dependencies as a separate step to take advantage of Docker's caching.
    # Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
    # Leverage a bind mount to requirements.txt to avoid having to copy them into
    # into this layer.
    RUN --mount=type=cache,target=/root/.cache/pip \
        --mount=type=bind,source=requirements.txt,target=requirements.txt \
        python -m pip install -r requirements.txt
    
    # Switch to the non-privileged user to run the application.
    USER appuser
    
    # Copy the source code into the container.
    COPY . .
    # Expose the port that the application listens on.
    EXPOSE 8501
    
    # Run the application.
    CMD ["streamlit", "run", "app.py"]

3. **You can then build and run the docker image**:
```bash
docker build -t export-assistance-ai .
docker run -d -p 8501:8501 export-assistance-ai
