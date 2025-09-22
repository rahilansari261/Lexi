# Jagriti States & Commissions API

A clean FastAPI service that provides access to states and district commissions from the Jagriti portal.

## Features

- **States API**: Get all available states and union territories
- **Commissions API**: Get district commissions for any state
- **Real-time Data**: Direct integration with Jagriti portal APIs
- **Swagger Documentation**: Interactive API documentation
- **Clean Architecture**: Minimal, focused implementation

## API Endpoints

### States
- `GET /states` - Get all available states with commission IDs

### Commissions  
- `GET /commissions/{state_id}` - Get district commissions for a specific state

### Documentation
- `GET /docs` - Interactive Swagger documentation
- `GET /redoc` - Alternative API documentation

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python main.py
```

The API will be available at `http://localhost:8000`

## Usage Examples

### Get All States
```bash
curl -X GET "http://localhost:8000/states"
```

### Get Commissions for Karnataka
```bash
curl -X GET "http://localhost:8000/commissions/11290000"
```

### View API Documentation
Open `http://localhost:8000/docs` in your browser for interactive Swagger documentation.

## Response Format

### States Response
```json
{
  "states": [
    {
      "commissionId": 11290000,
      "commissionNameEn": "KARNATAKA",
      "circuitAdditionBenchStatus": false,
      "activeStatus": true
    }
  ]
}
```

### Commissions Response
```json
{
  "commissions": [
    {
      "commissionId": 11290501,
      "commissionNameEn": "Bangalore Urban",
      "circuitAdditionBenchStatus": false,
      "activeStatus": true
    }
  ]
}
```

## Project Structure

```
jagriti-api/
├── main.py              # FastAPI application
├── jagriti_client.py    # Jagriti API client
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Technical Details

- **Framework**: FastAPI with automatic Swagger generation
- **HTTP Client**: httpx for async API calls
- **Data Source**: Direct integration with Jagriti portal APIs
- **Response Format**: Preserves original Jagriti API structure
- **Error Handling**: Graceful fallbacks with proper HTTP status codes

## API Integration

The API directly calls Jagriti portal endpoints:
- States: `https://e-jagriti.gov.in/services/report/report/getStateCommissionAndCircuitBench`
- Commissions: `https://e-jagriti.gov.in/services/report/report/getDistrictCommissionByCommissionId`

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is created for assessment purposes.

## Case Search APIs

### Case Search Endpoints

All case search endpoints accept the following request body:

```json
{
    "state": "KARNATAKA",
    "commission": "Bangalore Urban", 
    "search_value": "search_term",
    "judge_id": "3506",  // Only for judge search
    "page": 0,
    "size": 30,
    "from_date": "2025-01-01",
    "to_date": "2025-09-22"
}
```

#### Search by Case Number
- `POST /cases/by-case-number` - Search cases by case number

#### Search by Complainant
- `POST /cases/by-complainant` - Search cases by complainant name

#### Search by Respondent  
- `POST /cases/by-respondent` - Search cases by respondent name

#### Search by Complainant Advocate
- `POST /cases/by-complainant-advocate` - Search cases by complainant advocate name

#### Search by Respondent Advocate
- `POST /cases/by-respondent-advocate` - Search cases by respondent advocate name

#### Search by Industry Type
- `POST /cases/by-industry-type` - Search cases by industry type

#### Search by Judge
- `POST /cases/by-judge` - Search cases by judge (requires judge_id)

### Case Search Response Format

```json
{
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

### Usage Examples

#### Search by Case Number
```bash
curl -X POST "http://localhost:8000/cases/by-case-number" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "KARNATAKA",
    "commission": "Bangalore Urban",
    "search_value": "123/2025"
  }'
```

#### Search by Complainant
```bash
curl -X POST "http://localhost:8000/cases/by-complainant" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "KARNATAKA", 
    "commission": "Bangalore Urban",
    "search_value": "John Doe"
  }'
```

#### Search by Judge
```bash
curl -X POST "http://localhost:8000/cases/by-judge" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "KARNATAKA",
    "commission": "Bangalore Urban", 
    "search_value": "Judge Name",
    "judge_id": "3506"
  }'
```
