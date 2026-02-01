"""Tests for sweep measurement configuration models."""

from __future__ import annotations

import tunits

from measurement_config.models import (
    DataAcquisitionConfig,
    FrequencyConfig,
    ParameterSweepConfig,
    ParametricSequenceConfig,
    ParametricSequencePulseCommand,
    SweepMeasurementConfig,
)
from measurement_config.models.sweep_measurement_config import ParameterSweepContent


def _make_parametric_sequence() -> ParametricSequenceConfig:
    return ParametricSequenceConfig(
        delta_time=tunits.Time(4.0, "ns"),
        variable_list=["amp"],
        command_list=[
            ParametricSequencePulseCommand(
                name="pulse",
                channel_list=["q0"],
                argument_list=["amp", 0.5],
            )
        ],
    )


def _make_frequency_config() -> FrequencyConfig:
    return FrequencyConfig(
        channel_to_frequency={"q0": tunits.Frequency(5.0, "GHz")},
        channel_to_frequency_reference={"q0": "lo"},
        channel_to_frequency_shift={"q0": tunits.Frequency(0.1, "GHz")},
        keep_oscillator_relative_phase=True,
    )


def _make_data_acquisition() -> DataAcquisitionConfig:
    return DataAcquisitionConfig(
        shot_count=100,
        shot_repetition_margin=tunits.Time(1.0, "us"),
        data_acquisition_duration=tunits.Time(200.0, "ns"),
        data_acquisition_delay=tunits.Time(20.0, "ns"),
        data_acquisition_timeout=tunits.Time(10.0, "ms"),
        flag_average_waveform=True,
        flag_average_shots=False,
        delta_time=tunits.Time(4.0, "ns"),
        channel_to_averaging_time={"q0": tunits.Time(100.0, "ns")},
        channel_to_averaging_window={"q0": [0.0, 1.0, 2.0]},
    )


def _make_sweep_parameter() -> ParameterSweepConfig:
    content = ParameterSweepContent(
        category="frequency_shift",
        sweep_target=["q0"],
        value_list=[0.0, 0.1, 0.2],
    )
    return ParameterSweepConfig(
        sweep_content_list={"freq_shift": content},
        sweep_axis=[["freq_shift"]],
    )


def test_sweep_measurement_config_roundtrip():
    """Ensure sweep measurement config can be serialized and restored."""
    config = SweepMeasurementConfig(
        channel_list=["q0"],
        sequence=_make_parametric_sequence(),
        frequency=_make_frequency_config(),
        data_acquisition=_make_data_acquisition(),
        sweep_parameter=_make_sweep_parameter(),
    )

    data = config.to_dict()
    restored = SweepMeasurementConfig.from_dict(data)

    assert restored.channel_list == config.channel_list
    assert restored.sequence == config.sequence
    assert restored.frequency == config.frequency
    assert restored.data_acquisition == config.data_acquisition
    assert restored.sweep_parameter == config.sweep_parameter
