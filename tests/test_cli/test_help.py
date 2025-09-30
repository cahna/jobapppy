from .types import CliInvoke


def test_help(cli_invoke: CliInvoke):
    result = cli_invoke(["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout.strip()
