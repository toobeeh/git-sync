# git-sync

A small util that updates a git repository.  
Refer to the docker-compose.yml to see configuration via container env.

### Setup:

- create github webhook
- paste the docker container's URL (host:5000/webhook)
- choose a secret
- put the repo's git https clone url in the docker-compose
- put the webhook's secret in the docker-compose
- change the repository mount path in the docker-compose
  tests23
