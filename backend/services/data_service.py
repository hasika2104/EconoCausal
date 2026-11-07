from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.base_dir = BASE_DIR
        self.data_dir = self.base_dir / "data"
        self.processed_dir = self.data_dir / "processed"
        self.reports_dir = self.base_dir / "reports"
        self.models_dir = self.base_dir / "models"

        self._retail_df: Optional[pd.DataFrame] = None
        self._dml_results: Optional[Dict[str, Any]] = None
        self._sim_results: Optional[Dict[str, Any]] = None
        self._model_perf_df: Optional[pd.DataFrame] = None
        self._feature_analysis_df: Optional[pd.DataFrame] = None
        self._robustness_df: Optional[pd.DataFrame] = None
        self._recommendations_df: Optional[pd.DataFrame] = None
        self._product_analysis_df: Optional[pd.DataFrame] = None
        self._baseline_model = None

    def get_retail_data(self) -> pd.DataFrame:
        if self._retail_df is None:
            path = self.processed_dir / "retail_inventory_cleaned.csv"
            if not path.exists():
                path = self.data_dir / "retail_store_inventory-selected-columns.csv"
            if path.exists():
                df = pd.read_csv(path)
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
                if "Revenue" not in df.columns and "Price" in df.columns and "Units Sold" in df.columns:
                    df["Revenue"] = df["Price"] * df["Units Sold"]
                self._retail_df = df
            else:
                self._retail_df = pd.DataFrame()
        return self._retail_df

    def get_dml_results(self) -> Dict[str, Any]:
        if self._dml_results is None:
            path = self.processed_dir / "dml_validated_results.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._dml_results = json.load(f)
            else:
                self._dml_results = {}
        return self._dml_results

    def get_simulator_results(self) -> Dict[str, Any]:
        if self._sim_results is None:
            path = self.processed_dir / "pricing_simulator_results.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._sim_results = json.load(f)
            else:
                self._sim_results = {}
        return self._sim_results

    def get_model_performance(self) -> pd.DataFrame:
        if self._model_perf_df is None:
            path = self.reports_dir / "day16_model_performance.csv"
            if path.exists():
                self._model_perf_df = pd.read_csv(path)
            else:
                self._model_perf_df = pd.DataFrame()
        return self._model_perf_df

    def get_feature_analysis(self) -> pd.DataFrame:
        if self._feature_analysis_df is None:
            path = self.reports_dir / "day16_feature_analysis.csv"
            if path.exists():
                self._feature_analysis_df = pd.read_csv(path)
            else:
                self._feature_analysis_df = pd.DataFrame()
        return self._feature_analysis_df

    def get_robustness_results(self) -> pd.DataFrame:
        if self._robustness_df is None:
            path = self.reports_dir / "day15_robustness_results.csv"
            if path.exists():
                self._robustness_df = pd.read_csv(path)
            else:
                self._robustness_df = pd.DataFrame()
        return self._robustness_df

    def get_recommendations(self) -> pd.DataFrame:
        if self._recommendations_df is None:
            path = self.reports_dir / "day21_ai_pricing_recommendations.csv"
            if path.exists():
                self._recommendations_df = pd.read_csv(path)
            else:
                self._recommendations_df = pd.DataFrame()
        return self._recommendations_df

    def get_product_analysis(self) -> pd.DataFrame:
        if self._product_analysis_df is None:
            path = self.reports_dir / "day21_product_pricing_analysis.csv"
            if path.exists():
                self._product_analysis_df = pd.read_csv(path)
            else:
                self._product_analysis_df = pd.DataFrame()
        return self._product_analysis_df

    def get_baseline_model(self):
        if self._baseline_model is None:
            path = self.models_dir / "baseline_demand_model.joblib"
            if path.exists():
                try:
                    self._baseline_model = joblib.load(path)
                except Exception as e:
                    print(f"Error loading model: {e}")
                    self._baseline_model = None
        return self._baseline_model

data_service = DataService()
