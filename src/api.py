"""FastAPI lookup service for classification mappings."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from src.mapper import ClassificationMapper

app = FastAPI(
    title="Classification Bridge API",
    description="Map Australian Uniclass codes to NL-SfB (Table 1 + Table 3) and ETIM.",
    version="0.2.0",
)
mapper = ClassificationMapper()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/map/uniclass/{code}")
def map_from_uniclass(code: str):
    result = mapper.uniclass_to_crosswalk(code)
    if result.get("status") == "not_found":
        raise HTTPException(status_code=404, detail=result)
    return result


@app.get("/search/{query}")
def search_material(query: str):
    rows = mapper.search_by_name(query)
    if not rows:
        raise HTTPException(status_code=404, detail={"query": query, "results": []})
    results = [mapper.dict_to_result(row) for row in rows]
    return {"query": query, "count": len(results), "results": results}


@app.get("/materials")
def list_all_materials(
    review_status: Literal["draft", "verified", "needs_source"] | None = Query(
        default=None, description="Filter by review_status"
    ),
):
    rows = mapper.list_all(review_status=review_status)
    results = [mapper.dict_to_result(row) for row in rows]
    return {"count": len(results), "materials": results}
