from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.route("/states", methods=["GET"])
def get_states():
    """Get all available states with their internal IDs"""
    # Mock data for demonstration - in production this would scrape from Jagriti
    states = [
        {"id": "1", "name": "KARNATAKA"},
        {"id": "2", "name": "MAHARASHTRA"},
        {"id": "3", "name": "TAMIL NADU"},
        {"id": "4", "name": "DELHI"},
        {"id": "5", "name": "WEST BENGAL"}
    ]
    return jsonify({"states": states})

@app.route("/commissions/<state_id>", methods=["GET"])
def get_commissions(state_id):
    """Get all available commissions for a given state with their internal IDs"""
    # Mock data for demonstration - in production this would scrape from Jagriti
    commissions = [
        {"id": "1", "name": "Bangalore 1st & Rural Additional"},
        {"id": "2", "name": "Bangalore 2nd Additional"},
        {"id": "3", "name": "Mumbai 1st Additional"},
        {"id": "4", "name": "Chennai Additional"}
    ]
    return jsonify({"commissions": commissions})

@app.route("/cases/by-case-number", methods=["POST"])
def search_by_case_number():
    """Search cases by case number"""
    return search_cases("case_number", request.get_json())

@app.route("/cases/by-complainant", methods=["POST"])
def search_by_complainant():
    """Search cases by complainant name"""
    return search_cases("complainant", request.get_json())

@app.route("/cases/by-respondent", methods=["POST"])
def search_by_respondent():
    """Search cases by respondent name"""
    return search_cases("respondent", request.get_json())

@app.route("/cases/by-complainant-advocate", methods=["POST"])
def search_by_complainant_advocate():
    """Search cases by complainant advocate name"""
    return search_cases("complainant_advocate", request.get_json())

@app.route("/cases/by-respondent-advocate", methods=["POST"])
def search_by_respondent_advocate():
    """Search cases by respondent advocate name"""
    return search_cases("respondent_advocate", request.get_json())

@app.route("/cases/by-industry-type", methods=["POST"])
def search_by_industry_type():
    """Search cases by industry type"""
    return search_cases("industry_type", request.get_json())

@app.route("/cases/by-judge", methods=["POST"])
def search_by_judge():
    """Search cases by judge name"""
    return search_cases("judge", request.get_json())

def search_cases(search_type: str, request_data: Dict[str, Any]):
    """Common search function for all case search endpoints"""
    try:
        if not request_data:
            return jsonify({"error": "Request body is required"}), 400
            
        state = request_data.get("state", "")
        commission = request_data.get("commission", "")
        search_value = request_data.get("search_value", "")
        
        # Validate required fields
        if not state or not commission or not search_value:
            return jsonify({"error": "Missing required fields: state, commission, search_value"}), 400
        
        # Mock response for demonstration - in production this would scrape from Jagriti
        mock_cases = [
            {
                "case_number": "123/2025",
                "case_stage": "Hearing",
                "filing_date": "2025-02-01",
                "complainant": "John Doe",
                "complainant_advocate": "Adv. Reddy",
                "respondent": "XYZ Ltd.",
                "respondent_advocate": "Adv. Mehta",
                "document_link": "https://e-jagriti.gov.in/case/123/2025"
            },
            {
                "case_number": "456/2025",
                "case_stage": "Disposed",
                "filing_date": "2025-01-15",
                "complainant": "Jane Smith",
                "complainant_advocate": "Adv. Kumar",
                "respondent": "ABC Corp",
                "respondent_advocate": "Adv. Singh",
                "document_link": "https://e-jagriti.gov.in/case/456/2025"
            }
        ]
        
        # Filter based on search criteria (simplified for demo)
        filtered_cases = []
        for case in mock_cases:
            if search_value.lower() in case.get(search_type.replace("_", "_"), "").lower():
                filtered_cases.append(case)
        
        return jsonify(filtered_cases)
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)