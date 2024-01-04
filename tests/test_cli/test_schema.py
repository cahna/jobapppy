import json

import pytest


@pytest.mark.parametrize(
    "cmd_args",
    [
        pytest.param([], id="default"),
        pytest.param(["-i0"]),
        pytest.param(["-i1"]),
        pytest.param(["-i2"]),
    ],
)
def test_cli_schema(cmd_args, cli_invoke):
    result = cli_invoke(["schema", *cmd_args])
    assert result.exit_code == 0
    output = result.stdout.strip()
    assert output.startswith("{")
    assert output.endswith("}")
    data = json.loads(output)
    assert data
    assert data["$defs"]
