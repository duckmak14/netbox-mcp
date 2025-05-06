# Netbox MCP Server

A powerful integration server that combines Netbox's network infrastructure management capabilities with MCP (Multi-Cloud Platform) functionality. 

## Prerequisites

Ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
apt install python3.10-venv
git clone https://github.com/duckmak14/netbox-mcp.git
cd netbox-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root with the following variables:
```
NETBOX_URL=your_netbox_url
NETBOX_TOKEN=your_api_token
```
5. Start the server:
```bash
python server.py
```

6. Access the application at `http://localhost:8000`

### Option 2: Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/duckmak14/netbox-mcp.git
cd netbox-mcp
```

2. Configure environment variables:
Create a `.env` file in the project root with the following variables:
```
NETBOX_URL=your_netbox_url
NETBOX_TOKEN=your_api_token
```

3. Build and run with Docker Compose:
```markdown
**Note:** Starting from Docker Compose version 2.0, use the `docker compose` command. For older versions, use `docker-compose`.
```

```bash
# Build and start the container in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop the container
docker compose down
```

```markdown
**Note:** For older versions, use `docker-compose`.
```

```bash
# Build and start the container in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

4. Access the application at `http://localhost:8000`
