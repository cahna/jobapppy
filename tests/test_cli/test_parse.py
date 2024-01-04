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
def test_cli_parse(cmd_args, cli_invoke, tmp_path, example_resume_yaml_contents):
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(example_resume_yaml_contents)
    result = cli_invoke(["parse", str(resume_file), *cmd_args])
    assert result.exit_code == 0
