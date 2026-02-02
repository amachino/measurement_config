"""Tests for the Model and MutableModel classes."""

from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt
import tunits

from measurement_config.core import Model, MutableModel


class ExampleModel(Model):
    """Example model exercising custom serialization."""

    array: npt.NDArray[np.float64]
    complex_array: npt.NDArray[np.complex128]
    scalar: np.float64
    complex_scalar: np.complex128
    unit_value: tunits.Value
    unit_array: tunits.ValueArray
    time_value: tunits.Time
    frequency_array: tunits.FrequencyArray
    complex_list: list[complex]
    complex_value: complex
    metadata: dict[str, Any]


class SchemaModel(Model):
    """Model used to validate JSON schema generation."""

    array: npt.NDArray[np.float64]
    unit_value: tunits.Value


class MutableExample(MutableModel):
    """Simple mutable model for assignment tests."""

    value: int


def test_model_roundtrip_with_custom_types():
    """Roundtrip JSON/dict serialization for NumPy, tunits, and complex values."""
    model = ExampleModel(
        array=np.array([1.0, 2.0, 3.0]),
        complex_array=np.array([1 + 2j, 3 + 4j]),
        scalar=np.float64(1.25),
        complex_scalar=np.complex128(2 + 3j),
        unit_value=tunits.Value(5.0, "GHz"),
        unit_array=tunits.ValueArray([1, 2, 3], "ns"),
        time_value=tunits.Time(12.5, "ns"),
        frequency_array=tunits.FrequencyArray([1, 2, 3], "GHz"),
        complex_list=[1 + 2j, 3 + 4j],
        complex_value=3 + 4j,
        metadata={"label": "test"},
    )

    data = model.to_dict()
    assert data["array"]["__type__"].startswith("numpy.")
    assert data["complex_array"]["__type__"].startswith("numpy.")
    assert data["scalar"]["__type__"].startswith("numpy.")
    assert data["complex_scalar"]["__type__"].startswith("numpy.")
    assert data["unit_value"]["__type__"].startswith("tunits.")
    assert data["unit_array"]["__type__"].startswith("tunits.")
    assert data["time_value"]["__type__"].startswith("tunits.")
    assert data["frequency_array"]["__type__"].startswith("tunits.")
    assert data["complex_value"]["__type__"].startswith("python.")
    assert data["complex_list"][0]["__type__"].startswith("python.")

    restored = ExampleModel.from_dict(data)
    assert isinstance(restored.array, np.ndarray)
    assert isinstance(restored.complex_array, np.ndarray)
    assert isinstance(restored.scalar, np.generic)
    assert isinstance(restored.complex_scalar, np.generic)
    assert isinstance(restored.unit_value, tunits.Value)
    assert isinstance(restored.unit_array, tunits.ValueArray)
    assert isinstance(restored.time_value, tunits.Time)
    assert isinstance(restored.frequency_array, tunits.FrequencyArray)
    assert restored.complex_value == model.complex_value
    assert restored.complex_list == model.complex_list
    assert restored.metadata == model.metadata
    np.testing.assert_array_equal(restored.array, model.array)
    np.testing.assert_array_equal(restored.complex_array, model.complex_array)
    np.testing.assert_array_equal(restored.complex_scalar, model.complex_scalar)

    json_str = model.to_json(indent=2)
    restored_from_json = ExampleModel.from_json(json_str)
    np.testing.assert_array_equal(restored_from_json.array, model.array)
    np.testing.assert_array_equal(
        restored_from_json.complex_array,
        model.complex_array,
    )
    np.testing.assert_array_equal(
        restored_from_json.complex_scalar,
        model.complex_scalar,
    )
    assert restored_from_json.unit_value == model.unit_value
    np.testing.assert_array_equal(
        restored_from_json.unit_array.value,
        model.unit_array.value,
    )
    assert restored_from_json.unit_array.unit == model.unit_array.unit
    assert restored_from_json.time_value == model.time_value
    np.testing.assert_array_equal(
        restored_from_json.frequency_array.value,
        model.frequency_array.value,
    )
    assert restored_from_json.frequency_array.unit == model.frequency_array.unit
    assert restored_from_json.complex_value == model.complex_value
    assert restored_from_json.complex_list == model.complex_list


def test_json_schema_supports_custom_types():
    """Ensure JSON schema generation succeeds for NumPy and tunits types."""
    schema = SchemaModel.json_schema()
    assert schema["properties"]["array"]["type"] == "object"
    assert schema["properties"]["unit_value"]["type"] == "object"


def test_mutable_model_allows_assignment():
    """MutableModel should allow field updates."""
    model = MutableExample(value=1)
    model.value = 2
    assert model.value == 2
    assert MutableExample.model_config.get("frozen") is False
