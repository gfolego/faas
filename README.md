### About
In many Brazilian companies, we have to fill out the "*folha ponto*", which is basically a time sheet stating when we arrived at work, and when we left.
This is usually a cumbersome and merely bureaucratic task.

Facilitating this process, we released **Folha as a Service (FaaS)**.

**Contributions welcome**: check [open issues](https://github.com/gfolego/faas/issues)

**Contributors**: check [list](https://github.com/gfolego/faas/blob/master/CONTRIBUTORS.md)


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

