# Feline Folia Backend (Flask)

### Install

You need [Docker Community Edition](https://store.docker.com/search?offering=community&type=edition) installed.

When that is done installing, run these commands in your terminal:
```
docker-compose up --build
```

Then open a new terminal when that is finished building and type this to build the database:
```
docker-compose -f docker-compose.dev.yml exec website felinefolia db reset
```

### Development

You will only need to run the `--build` command when installing new packages so just use `docker-compose up`


### Config

We use a secret instance folder to configure secret keys. Ask an admin for this folder.


### Helpful SQL Commands

Get comments with user email
`SELECT comment, username FROM public.comments as c, public.users as u where c.user_id = u.id;`