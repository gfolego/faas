### About
In many Brazilian companies, we have to fill out the "*folha ponto*", which is basically a time sheet stating when we arrived at work, and when we left.
This is usually a cumbersome and merely bureaucratic task.

Facilitating this process, we released **Folha as a Service (FaaS)**.

Ideally, there will be a server where employees can submit their HR issued blank time sheet, and get it back completed. However, at this stage, we have only the script that performs the filling. Thus, contributions and feedback are always welcome!

Please note that this is *saturday afternoon* quality code, *i.e.*, it is primarily intended to work, rather been being fast, flexible or extensible.

### FaaS Standalone
##### Requirements
```bash
sudo apt-get install file poppler-utils bc ghostscript python
```

##### Using
```bash
bash src/faas.sh example/input.pdf example/output.pdf
```

### FaaS Server (REST API)
##### Requirements
```bash
sudo apt-get install python-flask
```

##### Starting server
```bash
python src/server.py
```

##### Using REST API
```bash
sudo apt-get install curl
curl --output 'example/output.pdf' --form 'file=@example/input.pdf' 'http://localhost:5000/'
```

### Future work (contributions welcome)
- Improve user experience
- Improve deployment
- Add logging (for future analytics)
- Convert `faas.sh` to Python
- Add personal signature
- Add personal handwriting style for numbers
- Add some stochastic variations

### Contributors (in alphabetical order)
- Bruno Ribeiro
- Fábio Beranizo (fabio.beranizo@gmail.com)
- Guilherme Folego (gfolego@gmail.com)
