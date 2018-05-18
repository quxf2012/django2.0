#启动redis
docker run -it --rm -p 6379:6379 --name=redis redis:alpine 
#连redis
docker exec -it redis  redis-cli
docker exec -it redis  redis-cli monitor  #持续监控
