import pytest


def test_build_errors_on_invalid_template_type():
    from jobapppy.environments import EnvironmentBuilder

    with pytest.raises(ValueError):
        EnvironmentBuilder().build("invalid-type")  # type: ignore[arg-type]
