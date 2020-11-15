# Raft DRF Exercise

This is a django-based api allows users to upload a pipe ("|") delimited text file containing order data to a PostgreSQL data base and retrieve previously uploaded order data. You will need python3 and postgreSQL install to run this api.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo DJANGO_SECRET_KEY="XXX" >> .env
echo DB_NAME="uploads" >> .env
echo DB_USER="" >> .env
echo DB_PASSWORD="" >> .env
echo DB_HOST="localhost" >> .env
echo DB_POST=5432 >> .env
```

Initialize and set up the database:

```bash
dropdb uploads
createdb uploads
```

## Usage

You can run this app either locally, in a Docker container, or deploy it to Heroku.

### Local

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: manage.py runserver
```

### Container

You will need the [Docker Engine](https://docs.docker.com/engine/install/) installed. On Ubuntu:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

You will also need [Docker Compose](https://docs.docker.com/compose/install/) installed. On Ubuntu:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Then running it as simple as:

```bash
docker-compose up
```

### Heroku

You will need the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed. On Ubuntu:

```bash
sudo snap install --classic heroku
```

Then you can setup PostgreSQL and deploy to Heroku.

```bash
heroku create raft-drf-exercise
heroku addons:create heroku-postgresql:hobby-dev --app raft-drf-exercise
heroku stack:set container
git push heroku main
```

## API Reference

The API reference documentation is available [here](https://documenter.getpostman.com/view/10868159/TVep8TFw?version=latest).

## Example

There is currently an example running on Heroku [here](https://raft-drf-exercise.herokuapp.com/).

## Testing Suite

The API has a testing suite to test all of the API endpoints.

To run all the tests:

```bash
Usage: manage.py test
```

## Credit

[Raft](https://goraft.tech/)

## License

Raft DRF Exercise is licensed under the [MIT license](https://github.com/danrneal/raft-drf-exercise/blob/master/LICENSE).
