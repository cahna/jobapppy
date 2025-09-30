# jobapppy

[![PyPI version](https://badge.fury.io/py/jobapppy.svg)](https://badge.fury.io/py/jobapppy)[![Python Versions](https://img.shields.io/pypi/pyversions/jobapppy?style=plastic)](https://pypi.org/project/jobapppy)
[![Main](https://github.com/cahna/jobapppy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/jobapppy/actions/workflows/main.yaml)

Tools to generate formatted resume documents (markdown, tex, pdf, etc) from yaml.

Documentation: [https://cahna.github.io/jobapppy](https://cahna.github.io/jobapppy)

## Installation

- pip:

   ```sh
   pip install jobapppy
   ```

- docker:

   ```sh
   docker pull ghcr.io/cahna/jobapppy:latest
   ```

## CLI Usage

- via script name installed in path:

   ```sh
   jobapppy --help
   ```

- as a python module:

   ```sh
   python -m jobapppy --help
   ```

- via docker:

   ```sh
   docker run --rm -it ghcr.io/cahna/jobapppy --help
   ```

## Tutorial

Create `resume.yaml`, then generate `resume.md` and/or `resume.tex` with `jobapppy`:

1. Create a `resume.yaml` file that satisfies jobapppy's schema
   - see `resume.example.yaml`
   - view the JSONSchema by running:

      ```sh
      jobapppy schema -i2
      ```

2. (optional) Check that `resume.yaml` can be parsed:

   ```sh
   jobapppy parse -c resume.yaml
   ```

3. Generate resume from templates:
   - Markdown (default, `-t md`)
      - Echo to stdout (default):

         ```sh
         jobapppy template resume.yaml
         ```

      - Echo to file:

         ```sh
         jobapppy template resume.yaml resume.md
         ```

   - Tex (`-t tex`)
      1. Generate `resume.tex`:

         ```sh
         jobapppy template -t tex resume.yaml resume.tex
         ```

      2. Generate `resume.pdf` using [cahna/jobapp](https://hub.docker.com/r/cahna/jobapp):

         ```sh
         docker run --rm -it -v "$(pwd):/data" --net=none --user="$(id -u):$(id -g)" cahna/jobapp lualatex -synctex=1 -interaction=nonstopmode resume.tex
         ```
