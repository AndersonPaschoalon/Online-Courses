#!/bin/bash


docker build -t devopsautomation:latest .
docker run -d -p 3000:3000 devopsautomation:latet
curl http://localhost:3000


