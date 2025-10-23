# 💱 Currency ETL Data Pipeline

A production-ready ETL (Extract, Transform, Load) pipeline that fetches real-time currency exchange rates from the Frankfurter API, processes the data with timezone conversions, and stores it in PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [CI/CD](#-cicd)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Real-time Data Extraction**: Fetches latest exchange rates from Frankfurter API
- **Timezone Management**: Automatic timezone conversion (UTC → Europe/Sofia)
- **Type Safety**: Robust data type conversion for PostgreSQL compatibility
- **Error Handling**: Comprehensive logging with Loguru
- **Dockerized**: Fully containerized with Docker Compose
- **Tested**: Unit tests with pytest and pytest-mock
- **CI/CD**: GitHub Actions workflow for automated testing
- **Database Management**: Automatic table creation and data insertion

## 🏗 Architecture

```
┌─────────────────┐
│  Frankfurter   │
│      API       │
└────────┬────────┘
         │ HTTP GET
         ▼
┌─────────────────┐
│   Requester    │ ← Fetches exchange rates
└────────┬────────┘
         │ JSON
         ▼
┌─────────────────┐
│     Worker     │ ← Transforms & processes data
└────────┬────────┘
         │ DataFrame
         ▼
┌─────────────────┐
│   DB Loader    │ ← Loads to PostgreSQL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL    │
│   Database     │
└─────────────────┘
```

## 📁 Project Structure

```
currency-etl-data-pipeline/
├── app/
│   ├── __init__.py
│   ├── config.py          # Environment configuration
│   ├── requester.py       # API data fetching
│   ├── worker.py          # Data transformation
│   ├── db_loader.py       # Database operations
│   └── helpers.py         # Utility functions
├── tests/
│   ├── test_requester.py
│   ├── test_worker.py
│   └── test_db_loader.py
├── docker/
│   ├── Dockerfile
│   └── compose.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.py                # Entry point
├── requirements.txt
├── pyproject.toml
├── .env                   # Environment variables
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Docker)
- Docker & Docker Compose (optional)

### Local Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/currency-etl-data-pipeline.git
cd currency-etl-data-pipeline
```

2. **Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the pipeline**

```bash
python main.py
```

### Docker Installation

1. **Start services**

```bash
cd docker
docker compose up --build
```

The pipeline will automatically:

- Create PostgreSQL database
- Create necessary tables
- Fetch and load exchange rate data

## ⚙ Configuration

Create a `.env` file in the project root:

```env
# API Configuration
API_URL=https://api.frankfurter.app/latest?from=USD

# Timezone Settings
ORIGINAL_TIMEZONE=UTC
TARGET_TIMEZONE=Europe/Sofia

# Database Configuration
DB_HOST=localhost          # Use 'db' for Docker
DB_PORT=5432
DB_NAME=etl_demo
DB_USER=postgres
DB_PASS=your_secure_password
```

### Environment Variables

| Variable            | Description              | Default      | Required |
| ------------------- | ------------------------ | ------------ | -------- |
| `API_URL`           | Frankfurter API endpoint | -            | ✅       |
| `ORIGINAL_TIMEZONE` | Source timezone          | UTC          | ❌       |
| `TARGET_TIMEZONE`   | Target timezone          | Europe/Sofia | ❌       |
| `DB_HOST`           | PostgreSQL host          | localhost    | ✅       |
| `DB_PORT`           | PostgreSQL port          | 5432         | ✅       |
| `DB_NAME`           | Database name            | etl_demo     | ✅       |
| `DB_USER`           | Database user            | postgres     | ✅       |
| `DB_PASS`           | Database password        | -            | ✅       |

## 💻 Usage

### Running the Pipeline

```bash
# Local execution
python main.py

# With Docker
docker compose -f docker/compose.yaml up

# Run in background
docker compose -f docker/compose.yaml up -d
```

### Accessing the Database

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d etl_demo

# View exchange rates
SELECT * FROM exchange_rates ORDER BY created_at DESC LIMIT 10;

# Check data for specific currency
SELECT * FROM exchange_rates WHERE currency = 'EUR';
```

## 🧪 Testing

The project includes comprehensive unit tests using `pytest` and `pytest-mock`.

### Run All Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run with output
pytest -s
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage in terminal
pytest --cov=app --cov-report=term

# Generate XML report for CI/CD
pytest --cov=app --cov-report=xml
```

### Run Specific Test File

```bash
# Test API fetching
pytest tests/test_requester.py -v

# Test data transformation
pytest tests/test_worker.py -v

# Test database operations
pytest tests/test_db_loader.py -v
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures (if needed)
├── test_requester.py     # API fetching tests
├── test_worker.py        # Data transformation tests
└── test_db_loader.py     # Database operation tests
```

### Test Coverage

| Module              | Description                           | Test Count |
| ------------------- | ------------------------------------- | ---------- |
| `test_requester.py` | API data fetching, error handling     | 5 tests    |
| `test_worker.py`    | Data transformation, type conversion  | 5 tests    |
| `test_db_loader.py` | Database connections, CRUD operations | 9 tests    |

### Key Test Scenarios

**Requester Tests**:

- ✅ Successful API data fetch
- ✅ HTTP timeout handling
- ✅ HTTP error responses (404, 500)
- ✅ Missing API URL configuration
- ✅ Invalid JSON response

**Worker Tests**:

- ✅ Successful data processing
- ✅ Empty/None input handling
- ✅ Missing 'rates' key
- ✅ Type conversion verification
- ✅ Timezone handling with mocked time

**DB Loader Tests**:

- ✅ Successful database connection
- ✅ Connection failure handling
- ✅ Table creation
- ✅ Data insertion
- ✅ Empty DataFrame handling
- ✅ None input handling
- ✅ Insert error handling

### Running Tests in Docker

```bash
# Run tests in Docker container
docker compose run --rm etl pytest

# With coverage
docker compose run --rm etl pytest --cov=app
```

## 🐳 Docker Deployment

### Build and Run

```bash
cd docker
docker compose up --build
```

### View Logs

```bash
docker compose logs -f etl
```

### Stop Services

```bash
docker compose down
```

### Remove Volumes

```bash
docker compose down -v
```

### Production Build

```bash
# Build for specific platform
docker build --platform=linux/amd64 -t currency-etl:latest -f docker/Dockerfile .

# Push to registry
docker tag currency-etl:latest your-registry/currency-etl:latest
docker push your-registry/currency-etl:latest
```

## 🔄 CI/CD

The project includes a GitHub Actions workflow that:

1. **Runs on**: Push and Pull Request events
2. **Tests**: Executes pytest suite
3. **Python Version**: 3.11

### Setting up CI/CD

1. Add secrets in GitHub repository settings:

   - `API_URL`: Frankfurter API endpoint

2. The workflow automatically:
   - Checks out code
   - Sets up Python environment
   - Installs dependencies with `uv`
   - Runs tests

## 🗄 Database Schema

### `exchange_rates` Table

| Column                 | Type                     | Description                    |
| ---------------------- | ------------------------ | ------------------------------ |
| `id`                   | SERIAL                   | Primary key                    |
| `currency`             | VARCHAR(10)              | Currency code (e.g., EUR, GBP) |
| `rate`                 | FLOAT                    | Exchange rate against USD      |
| `reference_date`       | DATE                     | Date of exchange rate          |
| `created_at`           | TIMESTAMP WITH TIME ZONE | UTC timestamp                  |
| `created_at_converted` | TIMESTAMP WITH TIME ZONE | Converted timezone timestamp   |

### Sample Query

```sql
-- Get latest rates
SELECT
    currency,
    rate,
    reference_date,
    created_at_converted
FROM exchange_rates
WHERE reference_date = CURRENT_DATE
ORDER BY currency;

-- Currency rate history
SELECT
    reference_date,
    rate
FROM exchange_rates
WHERE currency = 'EUR'
ORDER BY reference_date DESC
LIMIT 30;
```

## 📡 API Reference

### Frankfurter API

**Endpoint**: `https://api.frankfurter.app/latest`

**Parameters**:

- `from`: Base currency (default: USD)

**Response Format**:

```json
{
  "amount": 1.0,
  "base": "USD",
  "date": "2025-10-22",
  "rates": {
    "AUD": 1.5417,
    "BGN": 1.6879,
    "EUR": 0.85,
    ...
  }
}
```

## 🛠 Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (if available)
pre-commit install

# Run linting
flake8 app/ tests/

# Format code
black app/ tests/
```

### Adding New Features

1. Create feature branch
2. Implement changes in `app/`
3. Add tests in `tests/`
4. Run test suite
5. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings for functions
- Keep functions focused and small

## 🔧 Troubleshooting

### Common Issues

**Database Connection Failed**

```bash
# Check if PostgreSQL is running
docker ps

# Verify connection settings
psql -h localhost -U postgres -d etl_demo
```

**API Request Timeout**

```bash
# Test API manually
curl https://api.frankfurter.app
```
