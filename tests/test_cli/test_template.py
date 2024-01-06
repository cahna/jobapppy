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
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["template", str(resume_file), str(output_file), *cmd_args])
    assert result.exit_code == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_errors_on_invalid_template_type(cli_invoke, tmp_path, example_resume_yaml_contents):
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(example_resume_yaml_contents)
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["template", str(resume_file), str(output_file), "-t", "invalid-type"])
    assert result.exit_code == 2
    assert not output_file.exists()


def test_option_template_config(cli_invoke, tmp_path, example_resume_yaml_contents, get_template_path):
    test_config_file = tmp_path / "tmpl-config.json"
    test_config_file.write_text('{"replace_strings": {"test": "value"}}')
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(example_resume_yaml_contents)
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["template", "-c", str(test_config_file), str(resume_file), str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0
