

# AgroVerx API

## Prerequisites

- Docker
- Docker Compose
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/cardosorrenan/agroverx.git
cd agroverx
```

### 2. Configure env variables

Create a `.env` file:

```env
# .env file

POSTGRES_DB=agroverx
POSTGRES_USER=agroverxuser
POSTGRES_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True

```

### 3. Build and run the containers

```bash
docker-compose up --build
```

## Usage

### 1. API documentation

Available at `http://localhost:8000/v1/api/docs/` 

### 2. Example endpoints

- **Producers:** `/v1/api/producer/producer/`
- **Farms:** `/v1/api/producer/farm/`
- **Plantations:** `/v1/api/producer/farm-plantation/`
- **Dashboard Home:** `/v1/api/dashboard/home/`

### 3. Run tests

Use the following command:

```bash
 working...
```
