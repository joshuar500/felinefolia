# Feline Folia Backend (Flask)

### Install

You need [Docker Community Edition](https://store.docker.com/search?offering=community&type=edition) installed.

When that is done installing, run these commands in your terminal:

OSX:
```
./start.sh
```

WIN10:
```
./start.sh
```

Then open a new terminal when that is finished building and type this to build the database:
```
docker-compose -f docker-compose.dev.yml exec website felinefolia db reset
```

### Development

You can continue to use the `start.sh` or `start.bat` scripts, but if you want to run these manually, you can run:
```
docker-compose --build -f docker-compose.dev.yml up
```


### Config

We use a secret instance folder to configure secret keys. Ask Josh for this folder.


### Helpful SQL Commands

Get comments with user email
`SELECT comment, username FROM public.comments as c, public.users as u where c.user_id = u.id;`