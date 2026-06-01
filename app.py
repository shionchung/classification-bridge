"""Streamlit UI — material passport estimate without BIM."""

from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from data.au_building_stock import BUILDING_TYPES, MATERIAL_INTENSITIES
from src.material_estimator import MaterialPassportEstimator

BUILDING_LABELS = {
    "commercial_office": "Commercial office",
    "residential_detached": "Residential (detached house)",
    "residential_apartment": "Residential (apartment / flat)",
    "education": "Education (school / university)",
    "industrial_warehouse": "Industrial / warehouse",
}

st.set_page_config(
    page_title="AU Material Passport Estimator",
    page_icon="🏗️",
    layout="wide",
)

st.title("Material passport estimator (no BIM)")
st.caption(
    "Statistical urban-mining estimate for Australian buildings using type, "
    "floor area, and year built. Classification codes bridge Uniclass ↔ NL-SfB ↔ ETIM."
)

with st.sidebar:
    st.header("Building inputs")
    building_type = st.selectbox(
        "Building type",
        options=BUILDING_TYPES,
        format_func=lambda k: BUILDING_LABELS.get(k, k),
    )
    floor_area_m2 = st.number_input(
        "Gross floor area (m²)",
        min_value=1.0,
        value=3500.0,
        step=100.0,
    )
    year_built = st.number_input(
        "Year built",
        min_value=1900,
        max_value=datetime.now().year,
        value=1987,
        step=1,
    )
    postcode = st.text_input("Postcode (optional)", placeholder="e.g. 3000")
    run = st.button("Generate passport", type="primary", use_container_width=True)

    st.divider()
    st.markdown("**Data status**")
    st.warning(
        "Material intensities are research placeholders until populated from "
        "AHURI Report 402 and Stephan & Crawford literature. "
        "Edit `data/au_material_intensities.csv` and `data/au_building_stock_meta.csv`."
    )
    available = sorted({f"{bt} / {era}" for bt, era in MATERIAL_INTENSITIES})
    with st.expander(f"Available type × era combos ({len(available)})"):
        for row in available:
            st.text(row)

if run:
    estimator = MaterialPassportEstimator()
    passport = estimator.estimate(
        building_type=building_type,
        floor_area_m2=floor_area_m2,
        year_built=int(year_built),
        postcode=postcode or None,
    )

    if "error" in passport:
        st.error(passport["error"])
        if passport.get("available_keys"):
            st.info("Try one of these combinations:\n\n" + "\n".join(passport["available_keys"]))
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Era", passport["era"].replace("_", "–"))
        col2.metric("Confidence", passport.get("confidence", "—"))
        col3.metric("Materials", len(passport.get("materials", [])))
        total_kg = sum(m["estimated_kg"] for m in passport.get("materials", []))
        col4.metric("Total estimated mass", f"{total_kg:,.0f} kg")

        st.caption(f"Source: {passport.get('data_source', 'unknown')}")

        materials = passport.get("materials", [])
        if materials:
            st.subheader("Estimated materials")
            st.dataframe(
                materials,
                use_container_width=True,
                column_config={
                    "estimated_kg": st.column_config.NumberColumn(
                        "Estimated kg", format="%.1f"
                    ),
                    "kg_per_m2": st.column_config.NumberColumn(
                        "kg/m² GFA", format="%.2f"
                    ),
                },
            )

        st.subheader("JSON export")
        json_str = json.dumps(passport, indent=2)
        st.download_button(
            label="Download passport.json",
            data=json_str,
            file_name="material_passport.json",
            mime="application/json",
            use_container_width=True,
        )
        with st.expander("Preview JSON"):
            st.code(json_str, language="json")
else:
    st.info("Enter building details in the sidebar and click **Generate passport**.")

st.divider()
st.markdown(
    "#### Classification lookup (Project 4)\n"
    "Mappings live in `mappings/manual_mappings.csv`. "
    "Run the API with: `uvicorn src.api:app --reload`"
)
