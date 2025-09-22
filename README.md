# Lexi - Jagriti Case Search API

A FastAPI-based web service for searching and retrieving case information from the Jagriti portal. This API provides endpoints to search cases, get state information, and retrieve commission details.

## 🚀 Live Demo

- **Live API**: [https://lexi-production-3bd4.up.railway.app/docs](https://lexi-production-3bd4.up.railway.app/docs)
- **Demo Video**: [https://youtu.be/iYYrZ3VeKrA](https://youtu.be/iYYrZ3VeKrA)

## 📋 Features

- **Case Search**: Search for cases with various filters including date range, state, and commission
- **State Management**: Retrieve available states and their information
- **Commission Data**: Get commission details and related information
- **RESTful API**: Clean and well-documented REST endpoints
- **Interactive Documentation**: Built-in Swagger UI and ReDoc documentation
- **CORS Support**: Cross-origin resource sharing enabled for web applications

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **HTTPX**: Modern HTTP client for making requests
- **Python 3.8+**: Core programming language

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Lexi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional)**
   ```bash
   export DEBUG=True
   export LOG_LEVEL=DEBUG
   ```

## 🚀 Running the Application

### Development Mode

```bash
python main.py
```

The application will start on `http://localhost:8000`

### Using Uvicorn directly

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Root Endpoint**: `http://localhost:8000/`

## 🔧 Configuration

The application uses environment variables for configuration. Key settings can be found in `app/config.py`:

- `DEBUG`: Enable/disable debug mode
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## 📁 Project Structure

```
Lexi/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── cases.py          # Case search endpoints
│   │       ├── commissions.py    # Commission endpoints
│   │       └── states.py         # State endpoints
│   ├── middleware/
│   │   └── cors.py              # CORS configuration
│   ├── models/                  # Data models
│   ├── services/                # Business logic
│   ├── utils/                   # Utility functions
│   ├── config.py               # Application settings
│   └── main.py                 # FastAPI application
├── pdf_storage/                # PDF storage directory
├── tests/                      # Test files
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

## 📝 API Endpoints

### Core Endpoints

- `GET /` - API information and health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Case Search Endpoints

- `GET /api/v1/cases/search` - Search for cases with filters
- `GET /api/v1/cases/{case_id}` - Get specific case details

### State Endpoints

- `GET /api/v1/states` - Get all available states
- `GET /api/v1/states/{state_id}` - Get specific state information

### Commission Endpoints

- `GET /api/v1/commissions` - Get all commissions
- `GET /api/v1/commissions/{commission_id}` - Get specific commission details

## 🔒 CORS Configuration

The API is configured with permissive CORS settings for development. For production, consider restricting the `CORS_ORIGINS` setting in `app/config.py`.

## 🚀 Deployment

The application is currently deployed on Railway and accessible at:
[https://lexi-production-3bd4.up.railway.app/docs](https://lexi-production-3bd4.up.railway.app/docs)

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please open an issue in the GitHub repository or contact the development team.

---

**Note**: This API integrates with the Jagriti portal (https://e-jagriti.gov.in) to provide case search functionality. Please ensure you comply with their terms of service when using this API.
