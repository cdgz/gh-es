# Github ES inventory 

## Build image 
```
$ docker build -t gh-inventory .
```

## Init local swarm and create secrets
```
$ docker swarm init
$ echo "<GITHUB_TOKEN>" | base64 | docker secret create GH_ACCESS_TOKEN -
$ echo "<ES_XPACK_PASSWORD>" | base64 | docker secret create ES_XPACK_PASSWORD -
$ echo "<ES_XPACK_CA_CERT>" | base64 | docker secret create ES_XPACK_CA_CERT -
```

## Run
```
$ docker stack deploy -c stack.yml gh-stack 
```
To override ES user and host add `command: -U <ES_USER> -H <ES_URI>` in stack file
