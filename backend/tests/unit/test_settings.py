from pathlib import Path

import pytest

from solar_system.config import Settings


def test_data_dir_defaults_to_local_data_folder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SOLAR_DATA_DIR", raising=False)

    assert Settings().data_dir == Path("data")


def test_data_dir_can_be_overridden_with_an_environment_variable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("SOLAR_DATA_DIR", str(tmp_path))

    assert Settings().data_dir == tmp_path
