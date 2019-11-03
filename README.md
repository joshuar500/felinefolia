# Feline Folia Backend (Flask)

### Install

You need [Docker Community Edition](https://store.docker.com/search?offering=community&type=edition) installed.

When that is done installing, run these commands in your terminal (you may need to `chmod` for pemissions):

OSX:

```
python setup.py install
./start.sh
```

WIN10:

```
python setup.py install
start.bat
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

### Testing

We use tox to run tests. Make sure you have your dev environment up and running and then all you need to run is the following command:

```
tox
```

If you get an Invocation error, try deleting your `.tox` folder and try again.

### Notes
