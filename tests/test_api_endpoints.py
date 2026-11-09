"""
End-to-end API test suite for EconoCausal FastAPI backend
Verifies all 7 core functional endpoint groups and business logic.
"""

from pathlib import Path
import sys

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from starlette.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_dashboard_default():
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert "filters" in data
    assert "charts" in data
    assert data["kpis"]["total_products"] == 20
    assert data["kpis"]["dml_theta"] == 0.0107

def test_dashboard_with_filters():
    res = client.get("/api/dashboard?category=Electronics&region=North")
    assert res.status_code == 200
    data = res.json()
    assert data["kpis"]["total_records"] > 0

def test_eda():
    res = client.get("/api/eda")
    assert res.status_code == 200
    data = res.json()
    assert "summary_stats" in data
    assert "correlation_matrix" in data
    assert "distributions" in data
    assert len(data["distributions"]["price"]) > 0

def test_causal_analysis():
    res = client.get("/api/causal-analysis")
    assert res.status_code == 200
    data = res.json()
    assert data["spec1"]["theta_rounded"] == 0.0107
    assert data["spec2"]["theta_rounded"] == -0.0195
    assert len(data["robustness_specifications"]) == 18
    assert "feature_analysis" in data
    assert len(data["feature_analysis"]) == 9
    assert data["feature_analysis"][0]["feature"] == "Inventory Level"

def test_simulation_spec1():
    payload = {
        "product_id": "P0001",
        "current_price": 55.13,
        "proposed_price": 60.64,
        "inventory_level": 195.0,
        "cost_per_unit": 30.0,
        "specification": "spec1"
    }
    res = client.post("/api/simulate-price", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["simulation"]["proposed_price"] == 60.64
    assert data["profit_analysis"] is not None
    assert len(data["multi_scenario_grid"]) == 7
    assert "model_pipeline_evaluation" in data
    assert data["model_pipeline_evaluation"]["model_available"] is True
    assert data["model_pipeline_evaluation"]["ml_proposed_demand"] > 0

def test_recommendations():
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_segments"] == 100
    assert len(data["items"]) == 100

def test_products():
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.json()
    assert len(data["products"]) == 20

def test_dataset_preview():
    res = client.get("/api/dataset/preview?page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["rows"]) == 10
    assert data["total_rows"] == 73100
    assert "audit" in data
    assert data["audit"]["quality_score"] > 80

def test_dataset_validate():
    res = client.get("/api/dataset/validate")
    assert res.status_code == 200
    data = res.json()
    assert "quality_score" in data
    assert data["total_rows"] == 73100
    assert data["has_price"] is True
    assert data["has_units"] is True

def test_dataset_export_cleaned():
    res = client.get("/api/dataset/export-cleaned?format=csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]

def test_chat_ai_assistant():
    res = client.post("/api/chat", json={"message": "Which product has the highest demand?"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "demand" in data["reply"].lower() or "product" in data["reply"].lower()

def test_reports_summary():
    res = client.get("/api/reports/summary")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert "causal_dml" in data
    assert data["kpis"]["product_count"] == 20

def test_reports_export_excel():
    res = client.get("/api/reports/export?format=excel")
    assert res.status_code == 200
    assert "sheet" in res.headers["content-type"]

if __name__ == "__main__":
    test_health()
    test_dashboard_default()
    test_dashboard_with_filters()
    test_eda()
    test_causal_analysis()
    test_simulation_spec1()
    test_recommendations()
    test_products()
    test_dataset_preview()
    test_dataset_validate()
    test_dataset_export_cleaned()
    test_chat_ai_assistant()
    test_reports_summary()
    test_reports_export_excel()
    print("All 14 API endpoint test suites PASSED perfectly!")
