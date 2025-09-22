# Jagriti States & Commissions API

A FastAPI-based service that provides access to case data from the Jagriti portal (https://e-jagriti.gov.in) for District Consumer Courts (DCDRC) in India.

## 🏗️ Project Structure

```
Lexi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py              # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py            # Base models and common types
│   │   ├── state.py           # State-related models
│   │   ├── commission.py      # Commission-related models
│   │   └── case.py            # Case-related models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── jagriti_client.py  # Jagriti API client
│   │   └── case_service.py    # Business logic for case operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── states.py      # State endpoints
│   │   │   ├── commissions.py # Commission endpoints
│   │   │   └── cases.py       # Case search endpoints
│   │   └── dependencies.py    # Common dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── helpers.py         # Helper functions
│   └── middleware/
│       ├── __init__.py
│       └── cors.py            # CORS configuration
├── tests/
│   ├── __init__.py
│   └── test_models.py
├── requirements.txt
├── README.md
└── main.py                    # Entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Lexi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc
   - API Root: http://localhost:8000/

## 📚 API Endpoints

### States
- `GET /states` - Get all available states

### Commissions
- `GET /commissions/{state_id}` - Get commissions for a specific state

### Case Search
- `POST /cases/by-case-number` - Search by case number
- `POST /cases/by-complainant` - Search by complainant name
- `POST /cases/by-respondent` - Search by respondent name
- `POST /cases/by-complainant-advocate` - Search by complainant advocate
- `POST /cases/by-respondent-advocate` - Search by respondent advocate
- `POST /cases/by-industry-type` - Search by industry type
- `POST /cases/by-judge` - Search by judge

## 📝 Usage Examples

### Get States
```bash
curl -X GET "http://localhost:8000/states"
```

### Get Commissions for a State
```bash
curl -X GET "http://localhost:8000/commissions/11290000"
```

### Search Cases by Complainant
```bash
curl -X POST "http://localhost:8000/cases/by-complainant" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "KARNATAKA",
    "commission": "Bangalore 1st & Rural Additional",
    "search_value": "Reddy"
  }'
```

## 🔧 Configuration

The application can be configured through environment variables:

- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## 🧪 Testing

Run the tests:
```bash
pytest tests/
```

## 📋 Request/Response Models

### Case Search Request
```json
{
  "state": "KARNATAKA",
  "commission": "Bangalore 1st & Rural Additional",
  "search_value": "Reddy",
  "judge_id": "",
  "page": 0,
  "size": 30,
  "from_date": "2025-01-01",
  "to_date": "2025-09-22"
}
```

### Case Search Response
```json
{
  "success": true,
  "message": "Success",
  "cases": [
    {
      "case_number": "123/2025",
      "case_stage": "Hearing",
      "filing_date": "2025-02-01",
      "complainant": "John Doe",
      "complainant_advocate": "Adv. Reddy",
      "respondent": "XYZ Ltd.",
      "respondent_advocate": "Adv. Mehta",
      "document_link": "https://e-jagriti.gov.in/.../case123"
    }
  ],
  "total_count": 1,
  "page": 0,
  "size": 30
}
```

## 🏛️ Architecture

The application follows a clean architecture pattern:

- **Models**: Pydantic models for request/response validation
- **Services**: Business logic and external API integration
- **API**: FastAPI endpoints and routing
- **Utils**: Helper functions and custom exceptions
- **Middleware**: CORS and other middleware configurations

## 🔍 Error Handling

The API provides comprehensive error handling:

- **404**: State or commission not found
- **400**: Invalid request or search failed
- **500**: Internal server error

## 📊 Features

- ✅ Real-time data from Jagriti portal
- ✅ Multiple search types
- ✅ Pagination support
- ✅ Comprehensive error handling
- ✅ Swagger/OpenAPI documentation
- ✅ CORS enabled
- ✅ Clean architecture
- ✅ Type hints and validation
- ✅ Logging and monitoring

## 🚀 Deployment

The application can be deployed using:

- **Docker**: Create a Dockerfile and use Docker
- **Railway**: Deploy directly from GitHub
- **Heroku**: Use the Procfile
- **AWS/GCP/Azure**: Use container services

## 📄 License

This project is part of a take-home assessment for Lexi.

## 🤝 Contributing

This is a take-home assessment project. Please follow the submission guidelines provided in the assessment document.
