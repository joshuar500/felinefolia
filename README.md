# Feline Folia Backend (Flask)

### Install

You need [https://store.docker.com/search?offering=community&type=edition](Docker Community Edition) installed.

When that is done installing, run these commands in your terminal:
```
docker-compose up --build
```

Then open a new terminal when that is finished building and type this to build the database:
```
docker-compose exec website felinefolia db reset
```

### Development

You will only need to run the `--build` command when installing new packages so just use `docker-compose up`


### Config

We use a secret instance folder to configure secret keys. Ask an admin for this folder.


### Helpful SQL Commands

Get comments with user email
`SELECT comment, username FROM public.comments as c, public.users as u where c.user_id = u.id;`