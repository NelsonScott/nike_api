# (unofficial) nike_api

## Fetch Your Workout data from Nike (unofficial) api
1.  Go to https://www.nike.com/member/profile and login
1.  Open Chrome Dev tools, click Network, search NIKE.COM, under "Headers" copy the authorization 'bearer' value and copy it to 'bearer_token.txt'
1.  Run `./dev_scripts/docker.sh`
1.  Inside container run `./get_workouts.py`
1.  
