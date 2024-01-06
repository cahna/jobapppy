import pytest


def test_build_errors_on_invalid_template_type():
    from jobapppy.environments import EnvironmentBuilder, TemplateType

    with pytest.raises(ValueError):
        EnvironmentBuilder().build("invalid-type")
