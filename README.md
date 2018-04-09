# chess-rest
Chess game exposed through a web service

## Requirements
Requires flask-restplus and python-chess, use the provided requirements.txt file.
This service is compatible with Python >= 3.4

## Run
You can run the service directly with:

```
./main.py
```

A dockerfile is provided to help deploying this service. Build using the following command from the root of this repository:

```
docker build -t chess-rest:latest .
```

Run the container as follow:

```
docker run --rm -it --name my-chess-rest -p 9999:5000 chess-rest:latest
```
