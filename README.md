## About
In many Brazilian companies, we have to fill out the "*folha ponto*", which is basically a time sheet stating when we arrived at work, and when we left.
This is usually a cumbersome and merely bureaucratic task.

Facilitating this process, we released *Folha as a Service (FaaS)*.

**Contributions welcome**: check [open issues](https://github.com/gfolego/faas/issues)

**Contributors**: check [list](https://github.com/gfolego/faas/blob/master/CONTRIBUTORS.md)


## FaaS Deployment
This guide assumes [Docker](https://www.docker.com/) is properly installed and configured.

#### Build docker image
```bash
docker build --tag faas --file docker/Dockerfile --pull .
```

#### Run docker container
```bash
docker run --publish 5000:5000 --name faas faas
```

#### Using FaaS
Now, it is possible to access the web interface through http://localhost:5000.

It is also possible to access the REST API interface through command line:
```bash
curl --output 'example/output.pdf' --form 'file=@example/input.pdf' 'http://localhost:5000'
```

#### Updating FaaS
In case the repository is updated, just copy the new code to the docker container,
and [Gunicorn](http://gunicorn.org/) will reload the service automatically:
```bash
docker cp src/. faas:/faas
```
