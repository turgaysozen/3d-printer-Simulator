# 3D Printer Simulator

This project simulates a 3D printer environment where mock 3D printers generate random data. The real-time data is sent via WebSockets using Python Flask, and a static HTML page with JavaScript consumes and renders the data dynamically.

## Features

- Mock 3D Printer class generating random printer data.
- Real-time data transmission through WebSockets.
- HTML and JavaScript frontend for dynamic data rendering.
- Docker Compose for easy deployment.

## Prerequisites

- Docker and Docker Compose installed.
- Python and virtual environment for local development.

## Getting Started

### Local Development

1. Clone the repository:

    ```bash
    git clonehttps://github.com/turgaysozen/3d-printer-Simulator
    cd 3d-printer-simulator
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:

    ```bash
    python server.py
    ```

   The application will be accessible at `http://localhost:5000/3d-printer-simulation`.

### Docker Deployment

1. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

   The application will be accessible at `http://localhost:5000/3d-printer-simulation`.

## Usage

- Visit `http://localhost:5000/3d-printer-simulation` to view the 3D printer simulator dashboard.
- Real-time data will be updated and rendered dynamically on the page.
