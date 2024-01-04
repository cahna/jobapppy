from pathlib import Path
from typing import Callable, Union

import pytest


@pytest.fixture(scope="session", autouse=True)
def root_directory(request) -> Path:
    return Path(request.config.rootdir)


@pytest.fixture(scope="session", autouse=True)
def example_resume_yaml_file(root_directory: Path) -> Path:
    return root_directory / "resume.example.yaml"


@pytest.fixture(scope="session", autouse=True)
def example_resume_yaml_contents(example_resume_yaml_file: Path) -> str:
    return example_resume_yaml_file.read_text()


@pytest.fixture
def templates_dir(root_directory: Path) -> Path:
    """Path templates folder"""
    data_dir = root_directory / "jobapppy" / "templates"
    assert data_dir.is_dir()
    return data_dir


@pytest.fixture
def get_template_path(templates_dir: Path) -> Callable[[Union[str, Path]], Path]:
    """Provides a function to get the Path to a file in the tests data directory."""

    def get_data_file(filename: str | Path) -> Path:
        fpath = templates_dir / filename
        assert fpath.is_file()
        return fpath

    return get_data_file
