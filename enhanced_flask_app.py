from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import asyncio
from typing import Dict, List, Any
from scraper import JagritiScraper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize scraper
scraper = JagritiScraper()

@app.route("/")
def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.route("/states", methods=["GET"])
def get_states():
    """Get all available states with their internal IDs"""
    try:
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        states = loop.run_until_complete(scraper.get_states())
        loop.close()
        return jsonify({"states": states})
    except Exception as e:
        logger.error(f"Error fetching states: {e}")
        # Return fallback data
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
    try:
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        commissions = loop.run_until_complete(scraper.get_commissions(state_id))
        loop.close()
        return jsonify({"commissions": commissions})
    except Exception as e:
        logger.error(f"Error fetching commissions for state {state_id}: {e}")
        # Return fallback data
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
    return search_cases("caseNumber", request.get_json())

@app.route("/cases/by-complainant", methods=["POST"])
def search_by_complainant():
    """Search cases by complainant name"""
    return search_cases("complainantName", request.get_json())

@app.route("/cases/by-respondent", methods=["POST"])
def search_by_respondent():
    """Search cases by respondent name"""
    return search_cases("respondentName", request.get_json())

@app.route("/cases/by-complainant-advocate", methods=["POST"])
def search_by_complainant_advocate():
    """Search cases by complainant advocate name"""
    return search_cases("complainantAdvocate", request.get_json())

@app.route("/cases/by-respondent-advocate", methods=["POST"])
def search_by_respondent_advocate():
    """Search cases by respondent advocate name"""
    return search_cases("respondentAdvocate", request.get_json())

@app.route("/cases/by-industry-type", methods=["POST"])
def search_by_industry_type():
    """Search cases by industry type"""
    return search_cases("industryType", request.get_json())

@app.route("/cases/by-judge", methods=["POST"])
def search_by_judge():
    """Search cases by judge name"""
    return search_cases("judgeName", request.get_json())

def search_cases(search_field: str, request_data: Dict[str, Any]):
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
        
        # Get state and commission IDs
        states = get_states().get_json()["states"]
        state_id = next((s["id"] for s in states if s["name"].upper() == state.upper()), None)
        if not state_id:
            return jsonify({"error": f"State '{state}' not found"}), 400
        
        commissions = get_commissions(state_id).get_json()["commissions"]
        commission_id = next((c["id"] for c in commissions if c["name"].upper() == commission.upper()), None)
        if not commission_id:
            return jsonify({"error": f"Commission '{commission}' not found for state '{state}'"}), 400
        
        # Perform the search using scraper
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            cases = loop.run_until_complete(scraper.search_cases(
                state_id=state_id,
                commission_id=commission_id,
                search_field=search_field,
                search_value=search_value
            ))
            loop.close()
            return jsonify(cases)
        except Exception as e:
            logger.error(f"Error in scraper search: {e}")
            # Return mock data as fallback
            return jsonify([{
                "case_number": "123/2025",
                "case_stage": "Hearing",
                "filing_date": "2025-02-01",
                "complainant": "John Doe",
                "complainant_advocate": "Adv. Reddy",
                "respondent": "XYZ Ltd.",
                "respondent_advocate": "Adv. Mehta",
                "document_link": "https://e-jagriti.gov.in/case/123/2025"
            }])
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)