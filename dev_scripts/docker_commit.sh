docker commit $(docker ps -l | tail -1 | awk '{print $1}') nike_api
