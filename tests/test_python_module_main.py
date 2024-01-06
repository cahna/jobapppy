import runpy


def test_run_python_module():
    assert runpy.run_module("jobapppy")


def test_shell_run_as_python_module(shell):
    shell_result = shell.run("python", "-m", "jobapppy", "--help")
    assert shell_result.returncode == 0
