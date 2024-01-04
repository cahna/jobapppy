import pytest


@pytest.mark.parametrize(
    "cmd_args",
    [
        pytest.param([], id="default"),
        pytest.param(["-t", "md"]),
        pytest.param(["-t", "tex"]),
    ],
)
def test_cli_template(cmd_args, cli_invoke, tmp_path, example_resume_yaml_contents):
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(example_resume_yaml_contents)
    result = cli_invoke(["template", str(resume_file), *cmd_args])
    assert result.exit_code == 0
