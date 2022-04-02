#!/bin/bash

docker-compose down

docker rmi -f xaythixin/images:ucars-testing.staging.fe.latest

# docker rmi -f xaythixin/images:ucars-testing.staging.be.latest

docker pull xaythixin/images:ucars-testing.staging.fe.latest

# docker pull xaythixin/images:ucars-testing.staging.be.latest


docker-compose up -d
