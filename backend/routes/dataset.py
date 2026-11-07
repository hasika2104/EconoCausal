from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import Response
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import io
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/dataset", tags=["Dataset Explorer"])

# In-memory store for recently uploaded user files (session-based)
user_uploaded_dfs: Dict[str, pd.DataFrame] = {}

@router.get("/preview")
def get_dataset_preview(
    dataset_type: str = Query("default"), # "default" or upload_id
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
            raise HTTPException(status_code=404, detail="Uploaded dataset session not found")

    if df.empty:
        return {"rows": [], "total_rows": 0, "columns": [], "page": page, "page_size": page_size}

    filtered_df = df.copy()

    # Search filter across string columns
    if search:
        mask = np.column_stack([filtered_df[col].astype(str).str.contains(search, case=False, na=False) for col in filtered_df.columns])
        filtered_df = filtered_df[mask.any(axis=1)]

    # Sorting
    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(sort_by, ascending=(sort_dir == "asc"))

    total_rows = len(filtered_df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    page_slice = filtered_df.iloc[start_idx:end_idx]

    # Convert Date column to string if present
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

    return {
        "columns": columns_info,
        "rows": records,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": int(np.ceil(total_rows / page_size)) if total_rows > 0 else 1
    }

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    # Validation criteria
    validation_errors = []
    validation_warnings = []
    
    required_cols = ["Price", "Units Sold"]
    missing_required = [c for c in required_cols if c not in df.columns]
    if missing_required:
        validation_warnings.append(f"Standard pricing columns missing: {missing_required}. Simulation features will require these fields.")

    if len(df) < 10:
        validation_warnings.append("Dataset has fewer than 10 records. Statistical inference may be unreliable.")

    upload_id = f"upload_{len(user_uploaded_dfs) + 1}_{file.filename}"
    user_uploaded_dfs[upload_id] = df

    columns_info = []
    for col in df.columns:
        columns_info.append({
            "name": col,
            "type": str(df[col].dtype),
            "null_count": int(df[col].isna().sum()),
            "unique_count": int(df[col].nunique())
        })

    summary_stats = []
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols:
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
        "filename": file.filename,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": columns_info,
        "summary_stats": summary_stats,
        "validation": {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "warnings": validation_warnings
        }
    }

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
        mask = np.column_stack([filtered_df[col].astype(str).str.contains(search, case=False, na=False) for col in filtered_df.columns])
        filtered_df = filtered_df[mask.any(axis=1)]

    csv_data = filtered_df.to_csv(index=False)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=econocausal_export_{dataset_type}.csv"}
    )
