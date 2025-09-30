import json
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from pydantic import RootModel, TypeAdapter

from .environments import DEFAULT_TEMPLATE, EnvironmentBuilder, TemplateType
from .schemas import JobAppYaml, TemplateConfig

cli = typer.Typer()


@cli.command()
def parse(
    json_indent: Annotated[Optional[int], typer.Option("-i", help="Indentation for JSON output")] = None,
    check: Annotated[bool, typer.Option("-c", "--check", help="Do not output JSON, just check if valid")] = False,
    resume_yaml: Annotated[Optional[typer.FileText], typer.Argument(help="Yaml resume input")] = None,
    output_file: Annotated[Optional[typer.FileTextWrite], typer.Argument(help="Write output to file")] = None,
):
    """Parse a resume yaml file and output as JSON."""
    input_stream = resume_yaml if resume_yaml is not None else sys.stdin
    output_stream = output_file if output_file is not None else sys.stdout
    try:
        data = yaml.safe_load(input_stream)
        jobapp = JobAppYaml(**data)
    except Exception as e:
        if check:
            typer.echo("ERROR", err=True)
        else:
            typer.echo(f"Error parsing resume yaml: {e}", err=True)
        raise typer.Exit(code=1) from e
    if check:
        typer.echo("OK", err=True)
    else:
        typer.echo(RootModel[JobAppYaml](jobapp).model_dump_json(indent=json_indent), file=output_stream)


@cli.command()
def template(
    # template_file: Optional[Path] = typer.Option(..., "-f"),
    template_type: Annotated[TemplateType, typer.Option("-t", "--template-type")] = TemplateType.md,
    template_config: Annotated[
        Optional[Path], typer.Option("-c", "--template-config", help="Template configuration file (JSON)")
    ] = None,
    resume_yaml: Annotated[Optional[typer.FileText], typer.Argument(help="Yaml resume input")] = None,
    output_file: Annotated[Optional[typer.FileTextWrite], typer.Argument(help="Write output to file")] = None,
):
    """Render a resume from yaml input using a template."""
    input_stream = resume_yaml if resume_yaml is not None else sys.stdin
    output_stream = output_file if output_file is not None else sys.stdout
    tmpl_config: TemplateConfig = TemplateConfig(replace_strings={})
    template_file = DEFAULT_TEMPLATE[template_type]

    if template_config:
        json_text = template_config.read_text()
        json_data = json.loads(json_text)
        tmpl_config = TemplateConfig(**json_data)

    env = EnvironmentBuilder().build(template_type, tmpl_config.replace_strings)
    template = env.get_template(template_file)

    data = yaml.safe_load(input_stream)
    jobapp = JobAppYaml(**data)

    rendered_output = template.render(resume=jobapp.resume)
    typer.echo(rendered_output, file=output_stream)


@cli.command()
def schema(
    json_indent: Annotated[Optional[int], typer.Option("-i", help="Indentation for JSON output")] = None,
):
    """Output the JSON schema for the JobAppYaml schema."""
    typer.echo(json.dumps(TypeAdapter(JobAppYaml).json_schema(), indent=json_indent))
