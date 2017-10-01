### About
In many Brazilian companies, we have to fill out the "*folha ponto*", which is basically a time sheet stating when we arrived at work, and when we left.
This is usually a cumbersome and merely bureaucratic task.

Facilitating this process, we released **Folha as a Service (FaaS)**.

Ideally, there will be a server where employees can submit their HR issued blank time sheet, and get it back completed. However, at this stage, we have only the script that performs the filling. Thus, contributions and feedback are always welcome!

Please note that this is *saturday afternoon* quality code, *i.e.*, it is primarily intended to work, rather been being fast, flexible or extensible.

### Requirements
```bash
sudo apt-get install file poppler-utils bc pdfjam pdftk
```

### Using
```bash
bash src/faas.sh example/input.pdf example/output.pdf
```

### Future work (contributions welcome)
- Implement the actual "as a service"
- Add personal signature
- Add personal handwriting style for numbers
- Add some stochastic variations

### Extra
Images in `res` directory were taken from [https://www.1001freedownloads.com/free-cliparts/?order=new&tag=handwritten](https://www.1001freedownloads.com/free-cliparts/?order=new&tag=handwritten), and converted to PDF with `inkscape --without-gui --export-pdf=1.pdf 1.svg` (for each file).
