import functools

import pytest
from typer import Typer
from typer.testing import CliRunner


@pytest.fixture
def cli_entrypoint() -> Typer:
    """See: https://typer.tiangolo.com/tutorial/testing/#test-a-function"""
    from jobapppy.cli import cli

    return cli


@pytest.fixture
def cli_invoke(cli_entrypoint):
    runner = CliRunner()
    return functools.partial(runner.invoke, cli_entrypoint)
