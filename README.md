# measurement_config

Configuration models for quantum measurement setups. Built on `pydantic`, it supports JSON serialization/deserialization of values containing `tunits` and `numpy`, plus symbolic expression evaluation with `sympy`.

## Features

- Measurement configuration models (e.g., `SweepMeasurementConfig`)
- JSON serialization for `tunits` and `numpy` values
- Symbolic expression parsing/evaluation via `Expression`
- Unit helpers for frequency and time in `measurement_config.units`

## Installation

```shell
pip install "measurement_config @ git+https://github.com/amachino/measurement_config.git"
```

## Adding to pyproject.toml

This package can be added to [pyproject.toml](pyproject.toml) using the PEP 621 format.

```toml
[project]
dependencies = [
  "measurement_config @ git+https://github.com/amachino/measurement_config.git@v0.1.0",
]
```

## Usage

See [/docs/examples](docs/examples/) for usage examples.

## Development

### Setup

```shell
git clone https://github.com/amachino/measurement_config.git
cd measurement_config
make sync
```

### Test

```shell
make test
```

### Lint and type check

```shell
make check
```
