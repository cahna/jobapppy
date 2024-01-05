import pytest
import yaml


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
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["parse", str(resume_file), str(output_file), *cmd_args])
    assert result.exit_code == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0


@pytest.mark.parametrize(
    "cmd_options",
    [
        ["-c"],
        ["--check"],
    ],
)
def test_cli_parse_check_only(cmd_options, cli_invoke, tmp_path, example_resume_yaml_contents):
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(example_resume_yaml_contents)
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["parse", str(resume_file), *cmd_options])
    assert result.exit_code == 0
    assert not output_file.exists()


@pytest.mark.parametrize(
    "invalid_section_contents",
    [
        pytest.param("invalid", id="invalid"),
        pytest.param(None, id="null"),
        pytest.param(1, id="int"),
        pytest.param(1.0, id="float"),
        pytest.param(True, id="bool"),
    ],
)
def test_cli_parse_errors_on_invalid_section_contents(
    invalid_section_contents, cli_invoke, tmp_path, example_resume_yaml_contents
):
    resume_data = yaml.safe_load(example_resume_yaml_contents)
    resume_data["resume"]["sections"][0]["contents"] = invalid_section_contents
    resume_file = tmp_path / "test-resume.yml"
    resume_file.write_text(yaml.dump(resume_data))
    output_file = tmp_path / "test-resume.md"
    assert output_file.exists() is False
    result = cli_invoke(["parse", str(resume_file), str(output_file)])
    assert result.exit_code != 0
    assert not output_file.exists()


def test_error_loading_yaml(cli_invoke, tmp_path):
    resume_file = tmp_path / "test-invalid-content.yml"
    resume_file.write_text("invalid")
    result = cli_invoke(["parse", "-c", str(resume_file)])
    assert result.exit_code != 0
