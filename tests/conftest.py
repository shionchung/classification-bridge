"""Shared fixtures — isolated SQLite DB per test run."""

from __future__ import annotations

import pytest

from src.mapper import ClassificationMapper
from src.material_estimator import MaterialPassportEstimator


@pytest.fixture
def mapper(tmp_path):
    db = tmp_path / "test_mappings.db"
    return ClassificationMapper(db_path=db)


@pytest.fixture
def estimator(mapper):
    return MaterialPassportEstimator(mapper=mapper)
