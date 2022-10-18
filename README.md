## Online Polls for Kasetsart University (ku-polls)
[![Unittest](https://github.com/pinpimarn/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/pinpimarn/ku-polls/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/pinpimarn/ku-polls/branch/main/graph/badge.svg?token=M4T43MDT9P)](https://codecov.io/gh/pinpimarn/ku-polls)
This application is mainly used for online polls and surveys and using Django framework where you can see the tutorial on [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/). It also having other features as well.

## How to Install

Clone this repository into your local working space.

```
    git clone https://github.com/pinpimarn/ku-polls.git
```

Next, run
```
    python -m venv env
```
and
```
    . env/Scripts/activate
```

After that, you have to install the packages that are required for this repository.

```
    pip install -r requirements.txt
```

Next, deactivate the environment by

```
    deactivate
```

Then, you have to build your server using `settings.env`.

Lastly, you have to create the database run and load data by

```
    python manage.py loaddata data/polls.json data/users.json
```

## How to Run

You can run the server by

```
python ./manage.py runserver
```

Now, you can visit the link`http://localhost:8000`.

## Demo users

Users provided by the initial data (users.json):

| Username  | Password    |
|-----------|-------------|
| mymelody     | hackme22    |
| test     | iamabot555    |
| iamnewuser     | whatisthis000    |
| lestmetest    | helloworld222    |


## Project Documents

All project documents are in the [Project Wiki](https://github.com/pinpimarn/ku-polls/wiki)

- [Vision Statement](https://github.com/pinpimarn/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/pinpimarn/ku-polls/wiki/Requirements)
- [Project Plan](https://github.com/pinpimarn/ku-polls/wiki/Development-Plan)
- [Iteration 1 Plan](https://github.com/pinpimarn/ku-polls/wiki/Iteration-1-Plan) and [Iteration1](https://github.com/users/pinpimarn/projects/1/views/2)
- [Iteration 2 Plan](https://github.com/pinpimarn/ku-polls/wiki/Iteration-2-Plan) and [Iteration2](https://github.com/users/pinpimarn/projects/1/views/3)
- [Iteration 3 Plan](https://github.com/pinpimarn/ku-polls/wiki/Iteraton-3-Plan) and [Iteration3](https://github.com/users/pinpimarn/projects/1/views/4)
- [Iteration 4 Plan](https://github.com/pinpimarn/ku-polls/wiki/Iteraton-4-Plan) and [Iteration4](https://github.com/users/pinpimarn/projects/1/views/5)
