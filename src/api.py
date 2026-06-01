"""FastAPI lookup service for classification mappings."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from src.mapper import ClassificationMapper

app = FastAPI(
    title="Classification Bridge API",
    description="Map Australian Uniclass codes to NL-SfB and ETIM equivalents.",
    version="0.1.0",
)
mapper = ClassificationMapper()


@app.get("/", include_in_schema=False)
def root():
    """Browser-friendly entry point — raw JSON lives on the paths below."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/map/uniclass/{code}")
def map_from_uniclass(code: str):
    result = mapper.uniclass_to_nlsfb(code)
    if result.get("status") == "not_found":
        raise HTTPException(status_code=404, detail=result)
    return result


@app.get("/search/{query}")
def search_material(query: str):
    results = mapper.search_by_name(query)
    if not results:
        raise HTTPException(status_code=404, detail={"query": query, "results": []})
    return {"query": query, "count": len(results), "results": results}


@app.get("/materials")
def list_all_materials():
    materials = mapper.list_all()
    return {"count": len(materials), "materials": materials}
