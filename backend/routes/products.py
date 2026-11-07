from fastapi import APIRouter
import pandas as pd
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
def get_products():
    df = data_service.get_retail_data()
    if df.empty:
        return {"products": []}

    prod_grp = df.groupby("Product ID").agg(
        category=("Category", "first"),
        mean_price=("Price", "mean"),
        min_price=("Price", "min"),
        max_price=("Price", "max"),
        mean_demand=("Units Sold", "mean"),
        total_demand=("Units Sold", "sum"),
        mean_inventory=("Inventory Level", "mean"),
        total_revenue=("Revenue", "sum") if "Revenue" in df.columns else ("Units Sold", "count")
    ).reset_index()

    products = []
    for _, row in prod_grp.iterrows():
        products.append({
            "product_id": str(row["Product ID"]),
            "category": str(row["category"]),
            "mean_price": round(float(row["mean_price"]), 2),
            "min_price": round(float(row["min_price"]), 2),
            "max_price": round(float(row["max_price"]), 2),
            "mean_demand": round(float(row["mean_demand"]), 2),
            "total_demand": int(row["total_demand"]),
            "mean_inventory": round(float(row["mean_inventory"]), 2),
            "total_revenue": round(float(row["total_revenue"]), 2)
        })

    return {"products": sorted(products, key=lambda x: x["product_id"])}
