from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import io
import json
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/dataset", tags=["Dataset Explorer & Upload"])

# In-memory store for uploaded user files (session-based)
user_uploaded_dfs: Dict[str, pd.DataFrame] = {}
user_dataset_metadata: Dict[str, Dict[str, Any]] = {}

STANDARD_COLUMNS_MAP = {
    "product_id": ["Product ID", "product_id", "Product_ID", "SKU", "sku", "item_id", "Product"],
    "date": ["Date", "date", "Transaction_Date", "Sale_Date", "Day"],
    "price": ["Price", "price", "Unit_Price", "unit_price", "Selling_Price"],
    "units_sold": ["Units Sold", "units_sold", "Units_Sold", "Demand", "demand", "Quantity", "quantity", "Sales_Volume"],
    "revenue": ["Revenue", "revenue", "Total_Sales", "Sales", "sales"],
    "cost": ["Cost", "cost", "Unit_Cost", "unit_cost", "COGS", "cogs"],
    "inventory": ["Inventory Level", "inventory_level", "Inventory", "inventory", "Stock", "Stock_Level"],
    "promotion": ["Promotion", "promotion", "Discount", "discount", "Promo"],
    "competitor_price": ["Competitor_Price", "competitor_price", "Competitor Price", "Comp_Price"],
    "category": ["Category", "category", "Department", "dept", "Dept"],
    "region": ["Region", "region", "Store_Region", "Market"]
}

class ColumnMappingRequest(BaseModel):
    upload_id: str
    column_mappings: Dict[str, str] # e.g. {"sku": "product_id", "unit_price": "price"}

def detect_column_mappings(df: pd.DataFrame) -> Dict[str, str]:
    """Auto-detects closest standard column names for retail datasets."""
    detected = {}
    cols_lower = {str(c).lower().strip().replace(" ", "_").replace("-", "_"): c for c in df.columns}
    
    for standard_name, synonyms in STANDARD_COLUMNS_MAP.items():
        matched_actual = None
        for syn in synonyms:
            syn_norm = syn.lower().replace(" ", "_").replace("-", "_")
            if syn_norm in cols_lower:
                matched_actual = cols_lower[syn_norm]
                break
        if matched_actual:
            detected[matched_actual] = standard_name
    return detected

def run_data_audit(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes comprehensive retail dataset quality audit and metrics."""
    total_rows = len(df)
    total_cols = len(df.columns)
    
    if total_rows == 0:
        return {
            "quality_score": 0,
            "total_rows": 0,
            "total_cols": 0,
            "duplicate_rows": 0,
            "duplicate_pct": 0.0,
            "missing_cells": 0,
            "missing_pct": 0.0,
            "issues": ["Dataset is empty."],
            "warnings": [],
            "column_audits": []
        }

    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = round((duplicate_rows / total_rows) * 100, 2)
    
    total_cells = total_rows * total_cols
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2)
    
    issues = []
    warnings = []
    column_audits = []
    
    # Check key columns
    detected_mappings = detect_column_mappings(df)
    has_price = any(v == "price" for v in detected_mappings.values())
    has_units = any(v == "units_sold" for v in detected_mappings.values())
    has_date = any(v == "date" for v in detected_mappings.values())
    has_cost = any(v == "cost" for v in detected_mappings.values())
    
    if not has_price:
        issues.append("Missing required 'Price' column for pricing analytics and causal inference.")
    if not has_units:
        issues.append("Missing required 'Units Sold' or 'Demand' column for elasticity estimation.")
    if not has_date:
        warnings.append("Date column not detected. Temporal trends will be restricted to sequential order.")
    if not has_cost:
        warnings.append("Cost column not detected. Profit and gross margin analytics will be unavailable or estimated.")

    # Column-level audit
    invalid_val_count = 0
    for col in df.columns:
        s = df[col]
        null_count = int(s.isna().sum())
        null_pct = round((null_count / total_rows) * 100, 2)
        unique_count = int(s.nunique())
        col_type = str(s.dtype)
        
        is_num = pd.api.types.is_numeric_dtype(s)
        neg_count = 0
        zero_count = 0
        outliers_count = 0
        
        if is_num:
            neg_count = int((s < 0).sum())
            zero_count = int((s == 0).sum())
            if neg_count > 0 and ("price" in col.lower() or "sold" in col.lower() or "inventory" in col.lower()):
                invalid_val_count += neg_count
                issues.append(f"Column '{col}' has {neg_count} negative values where strictly positive is required.")
            
            # IQR outlier check
            q25 = s.quantile(0.25)
            q75 = s.quantile(0.75)
            iqr = q75 - q25
            if iqr > 0:
                outliers_count = int(((s < (q25 - 3 * iqr)) | (s > (q75 + 3 * iqr))).sum())
        
        column_audits.append({
            "name": col,
            "type": col_type,
            "is_numeric": is_num,
            "null_count": null_count,
            "null_pct": null_pct,
            "unique_count": unique_count,
            "negative_count": neg_count,
            "zero_count": zero_count,
            "outliers_count": outliers_count,
            "mapped_to": detected_mappings.get(col, None)
        })

    # Calculate overall health score (0 to 100)
    score = 100.0
    score -= min(30.0, missing_pct * 1.5)
    score -= min(20.0, duplicate_pct * 2.0)
    if not has_price:
        score -= 25.0
    if not has_units:
        score -= 25.0
    if invalid_val_count > 0:
        score -= min(15.0, (invalid_val_count / total_rows) * 100)
    score = max(0.0, min(100.0, round(score, 1)))

    return {
        "quality_score": score,
        "total_rows": total_rows,
        "total_cols": total_cols,
        "duplicate_rows": duplicate_rows,
        "duplicate_pct": duplicate_pct,
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "has_price": has_price,
        "has_units": has_units,
        "has_cost": has_cost,
        "has_date": has_date,
        "detected_mappings": detected_mappings,
        "issues": issues,
        "warnings": warnings,
        "column_audits": column_audits
    }

@router.get("/preview")
def get_dataset_preview(
    dataset_type: str = Query("default"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=5, le=100),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("asc"),
    search: Optional[str] = Query(None)
):
    if dataset_type == "default":
        df = data_service.get_retail_data()
    else:
        df = user_uploaded_dfs.get(dataset_type)
        if df is None:
            raise HTTPException(status_code=404, detail="Dataset session not found or expired")

    if df.empty:
        return {"rows": [], "total_rows": 0, "columns": [], "page": page, "page_size": page_size}

    filtered_df = df.copy()

    # Search filter across string columns
    if search:
        search_str = search.strip().lower()
        masks = []
        for col in filtered_df.columns:
            masks.append(filtered_df[col].astype(str).str.lower().str.contains(search_str, na=False, regex=False))
        if masks:
            combined_mask = np.logical_or.reduce(masks)
            filtered_df = filtered_df[combined_mask]

    # Sorting
    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(sort_by, ascending=(sort_dir == "asc"))

    total_rows = len(filtered_df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    page_slice = filtered_df.iloc[start_idx:end_idx]

    records = []
    for _, row in page_slice.iterrows():
        row_dict = {}
        for col in filtered_df.columns:
            val = row[col]
            if pd.isna(val):
                row_dict[col] = None
            elif isinstance(val, (pd.Timestamp, np.datetime64)):
                row_dict[col] = val.strftime("%Y-%m-%d")
            elif isinstance(val, (np.integer, int)):
                row_dict[col] = int(val)
            elif isinstance(val, (np.floating, float)):
                row_dict[col] = round(float(val), 2)
            else:
                row_dict[col] = str(val)
        records.append(row_dict)

    columns_info = []
    for col in df.columns:
        columns_info.append({
            "name": col,
            "type": str(df[col].dtype),
            "null_count": int(df[col].isna().sum()),
            "unique_count": int(df[col].nunique())
        })

    audit = run_data_audit(df)

    return {
        "columns": columns_info,
        "rows": records,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": int(np.ceil(total_rows / page_size)) if total_rows > 0 else 1,
        "audit": audit
    }

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_data.csv"
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    if ext not in ["csv", "xlsx", "xls"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a .csv, .xlsx, or .xls file.")

    content = await file.read()
    # 25 MB safety limit
    if len(content) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum permitted limit of 25MB.")

    try:
        if ext == "csv":
            try:
                df = pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding="latin-1")
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse tabular file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file contains no data rows.")

    upload_id = f"upload_{len(user_uploaded_dfs) + 1}_{filename.replace(' ', '_')}"
    user_uploaded_dfs[upload_id] = df

    audit = run_data_audit(df)
    user_dataset_metadata[upload_id] = {
        "filename": filename,
        "upload_id": upload_id,
        "rows": len(df),
        "columns": len(df.columns),
        "audit": audit
    }

    summary_stats = []
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols[:8]:
        s = df[col]
        summary_stats.append({
            "column": col,
            "mean": round(float(s.mean()), 2) if not pd.isna(s.mean()) else None,
            "std": round(float(s.std()), 2) if not pd.isna(s.std()) else None,
            "min": round(float(s.min()), 2) if not pd.isna(s.min()) else None,
            "max": round(float(s.max()), 2) if not pd.isna(s.max()) else None
        })

    return {
        "status": "success",
        "upload_id": upload_id,
        "filename": filename,
        "row_count": len(df),
        "column_count": len(df.columns),
        "summary_stats": summary_stats,
        "audit": audit
    }

@router.post("/map-columns")
def map_columns(req: ColumnMappingRequest):
    df = user_uploaded_dfs.get(req.upload_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset session not found")

    rename_dict = {}
    standard_labels = {
        "product_id": "Product ID",
        "date": "Date",
        "price": "Price",
        "units_sold": "Units Sold",
        "revenue": "Revenue",
        "cost": "Cost",
        "inventory": "Inventory Level",
        "promotion": "Promotion",
        "competitor_price": "Competitor_Price",
        "category": "Category",
        "region": "Region"
    }

    for orig_col, target_key in req.column_mappings.items():
        if orig_col in df.columns and target_key in standard_labels:
            rename_dict[orig_col] = standard_labels[target_key]

    mapped_df = df.rename(columns=rename_dict)
    
    # Calculate Revenue if Price and Units Sold are now mapped and Revenue is not
    if "Revenue" not in mapped_df.columns and "Price" in mapped_df.columns and "Units Sold" in mapped_df.columns:
        try:
            mapped_df["Revenue"] = pd.to_numeric(mapped_df["Price"], errors="coerce") * pd.to_numeric(mapped_df["Units Sold"], errors="coerce")
        except Exception:
            pass

    user_uploaded_dfs[req.upload_id] = mapped_df
    new_audit = run_data_audit(mapped_df)
    
    return {
        "status": "success",
        "upload_id": req.upload_id,
        "mapped_columns": rename_dict,
        "audit": new_audit
    }

@router.get("/validate")
def validate_dataset(dataset_type: str = Query("default")):
    if dataset_type == "default":
        df = data_service.get_retail_data()
    else:
        df = user_uploaded_dfs.get(dataset_type)
        if df is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
    
    return run_data_audit(df)

@router.get("/export-cleaned")
def export_cleaned_dataset(
    dataset_type: str = Query("default"),
    drop_duplicates: bool = Query(True),
    fill_missing: bool = Query(True),
    format: str = Query("csv")
):
    if dataset_type == "default":
        df = data_service.get_retail_data()
    else:
        df = user_uploaded_dfs.get(dataset_type)
        if df is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

    cleaned_df = df.copy()
    if drop_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()

    if fill_missing:
        for col in cleaned_df.columns:
            if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            else:
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    if format == "xlsx":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
        output.seek(0)
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=cleaned_{dataset_type}.xlsx"}
        )
    else:
        csv_data = cleaned_df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=cleaned_{dataset_type}.csv"}
        )

@router.get("/export")
def export_dataset(
    dataset_type: str = Query("default"),
    search: Optional[str] = Query(None)
):
    if dataset_type == "default":
        df = data_service.get_retail_data()
    else:
        df = user_uploaded_dfs.get(dataset_type)
        if df is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

    filtered_df = df.copy()
    if search:
        search_str = search.strip().lower()
        masks = [filtered_df[col].astype(str).str.lower().str.contains(search_str, na=False, regex=False) for col in filtered_df.columns]
        if masks:
            filtered_df = filtered_df[np.logical_or.reduce(masks)]

    csv_data = filtered_df.to_csv(index=False)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=econocausal_export_{dataset_type}.csv"}
    )
