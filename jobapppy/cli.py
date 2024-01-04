import json
import sys
from pathlib import Path
from typing import Optional

import typer
import yaml

from .environments import DEFAULT_TEMPLATE, EnvironmentBuilder, TemplateType
from .filters import make_tex_escape
from .schemas import JobAppYaml, TemplateConfig

cli = typer.Typer()


@cli.command()
def template(
    # template_file: Optional[Path] = typer.Option(..., "-f"),
    template_type: TemplateType = typer.Option(TemplateType.md, "-t"),
    template_config: Optional[Path] = typer.Option(None, "-c", help="Template configuration file (JSON)"),
    resume_yaml: typer.FileText = typer.Argument(sys.stdin, help="Yaml resume input"),
    output_file: typer.FileTextWrite = typer.Argument(sys.stdout, help="Write output to file"),
):
    tmpl_config: TemplateConfig = TemplateConfig(replace_strings={})
    template_file = DEFAULT_TEMPLATE[template_type]

    if template_config:
        json_text = template_config.read_text()
        json_data = json.loads(json_text)
        tmpl_config = TemplateConfig(**json_data)

    env = EnvironmentBuilder().build(template_type, tmpl_config.replace_strings)
    template = env.get_template(template_file)

    data = yaml.safe_load(resume_yaml)
    jobapp = JobAppYaml(**data)

    rendered_output = template.render(resume=jobapp.resume)
    output_file.write(rendered_output)
