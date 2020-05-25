# (unofficial) nike_api

![Nike Workout Data Example](Images/workouts-example.png)
## Fetch Your Workout data from Nike (unofficial) api
1.  Go to https://www.nike.com/member/profile and login
1.  Open Chrome Dev tools, click Network, search NIKE.COM, under "Headers" copy the authorization 'bearer' value and copy it to 'bearer_token.txt'. (you may need to refresh)
1.  Run `./scripts/get_workouts.sh`
1.  And finally, open nike-workouts.html in Chrome
