"""Tests for sweep measurement result model."""

from __future__ import annotations

import numpy as np

from measurement_config.models import SweepMeasurementResult


def test_sweep_measurement_result_roundtrip():
    """Ensure result data can be serialized and restored."""
    result = SweepMeasurementResult(
        metadata={"experiment": "rabi"},
        data=np.array([[1.0, 2.0], [3.0, 4.0]]),
        data_shape=[2, 2],
        sweep_key_list=["freq_shift"],
        data_key_list=["signal"],
    )

    payload = result.to_dict()
    assert payload["data"]["__type__"].startswith("numpy.")

    restored = SweepMeasurementResult.from_dict(payload)
    np.testing.assert_array_equal(restored.data, result.data)
    assert restored.metadata == result.metadata
    assert restored.data_shape == result.data_shape
    assert restored.sweep_key_list == result.sweep_key_list
    assert restored.data_key_list == result.data_key_list
