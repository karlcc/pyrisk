## Perform Metric for Stock Portfolio

### Python/Flask application

Project structure:
```
.
├── Dockerfile
├── requirements.txt
├── app
    ├── apikey.py
    ├── config.py
    └── main.py

```

## Deploy with docker

```
docker run -dp 8001:8001 karl8080/pyrisk
```

## Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                    NAMES
78e6c069e2f3   pyrisk    "flask --app app.mai…"   7 seconds ago   Up 4 seconds   0.0.0.0:8001->8001/tcp   optimistic_meninsky
```

After the application starts, navigate to `http://localhost:8001` in your web browser or run:
```
$ curl localhost:8000
Stock: spy
Periods: 2019-1-1 to 2021-1-1
Fixed Fraction(%): 20.0, CAR25(%): 2.164
```

Navigate to `http://localhost:8001/eq` in your web browser to check the simulated equity curves:
```

```
