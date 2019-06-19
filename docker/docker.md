# Docker for c++ development

Create a dockerfile to run your app:

```dockerfile
FROM gcc
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN gcc -o myapp main.c
CMD ["./myapp"]
```

```
docker build -t my-gcc-app .
docker run -it --rm --name my-running-app my-gcc-app
docker image rm my-gcc-app
```