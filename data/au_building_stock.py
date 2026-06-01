"""
Australian building material intensities (kg/m² GFA) by type and era.

PLACEHOLDER VALUES — replace with literature-backed figures from:
- AHURI Final Report 402 (Building materials in a circular economy)
- Stephan & Crawford (University of Melbourne) material stock analyses

Keys: (building_type, era) -> {material_key: kg_per_m2, _confidence, _source}
"""

MATERIAL_INTENSITIES: dict[tuple[str, str], dict] = {
    ("commercial_office", "1960_1979"): {
        "structural_steel": 45,
        "reinforced_concrete": 820,
        "float_glass": 18,
        "aluminium": 8,
        "plasterboard": 12,
        "carpet": 4,
        "_confidence": "low",
        "_source": "PLACEHOLDER — populate from AHURI Report 402",
    },
    ("commercial_office", "1980_1999"): {
        "structural_steel": 52,
        "reinforced_concrete": 890,
        "float_glass": 22,
        "aluminium": 10,
        "plasterboard": 14,
        "carpet": 5,
        "_confidence": "low",
        "_source": "PLACEHOLDER — AHURI 402 + Stephan & Crawford",
    },
    ("commercial_office", "2000_2009"): {
        "structural_steel": 48,
        "reinforced_concrete": 750,
        "float_glass": 25,
        "aluminium": 12,
        "plasterboard": 15,
        "mineral_wool": 3,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("residential_detached", "1960_1979"): {
        "softwood_timber": 28,
        "brick_clay": 210,
        "concrete_slab": 380,
        "plasterboard": 8,
        "carpet": 6,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("residential_detached", "1980_1999"): {
        "softwood_timber": 32,
        "brick_clay": 180,
        "concrete_slab": 420,
        "plasterboard": 10,
        "vinyl_flooring": 4,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("residential_detached", "2000_2009"): {
        "softwood_timber": 35,
        "brick_clay": 150,
        "concrete_slab": 400,
        "plasterboard": 12,
        "eps_insulation": 2,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("industrial_warehouse", "1980_1999"): {
        "structural_steel": 85,
        "precast_concrete": 120,
        "galvanised_steel": 15,
        "concrete_slab": 450,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("industrial_warehouse", "2000_2009"): {
        "structural_steel": 75,
        "precast_concrete": 100,
        "galvanised_steel": 18,
        "concrete_slab": 400,
        "mineral_wool": 2,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
    ("industrial_warehouse", "2010_present"): {
        "structural_steel": 70,
        "precast_concrete": 90,
        "galvanised_steel": 20,
        "concrete_slab": 380,
        "eps_insulation": 3,
        "_confidence": "low",
        "_source": "PLACEHOLDER",
    },
}

BUILDING_TYPES = [
    "commercial_office",
    "residential_detached",
    "industrial_warehouse",
]

ERAS = ["pre_1960", "1960_1979", "1980_1999", "2000_2009", "2010_present"]
