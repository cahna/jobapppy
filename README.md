# jobapppy


## How to

### Generate resume PDF

1. `jobapppy -t tex resume.example.yaml resume.example.tex`
2. ```sh
   docker run --rm -it -v "$(pwd):/data" --net=none --user="$(id -u):$(id -g)" cahna/jobapp lualatex -synctex=1 -interaction=nonstopmode resume.example.tex
   ```
