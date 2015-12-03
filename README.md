# Yanlog
[![Build Status](https://circleci.com/gh/janusle/yanlog.svg?style=shield&circle-token=6edbd235aecaa8db636ae888a6b13a8f9d510a47)](https://circleci.com/gh/janusle/yanlog)

A personal blog built with Django.

## Main Stack

+ [Django](https://www.djangoproject.com/)
+ [Bootstrap](http://getbootstrap.com/)
+ [Markdown](https://github.com/trentm/python-markdown2)
+ [EpicEditor](http://epiceditor.com/)
+ [Code syntax highlighting](https://github.com/trentm/python-markdown2/wiki/fenced-code-blocks)
+ [Disqus](https://disqus.com/)


## Development Prerequisites

+ [docker](https://www.docker.com/)
+ [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
+ python-dev(apt)
+ libpq-dev(apt)


## Development Setup

```bash
$ mkvirtualenv yanlog

# Install all dependencies
$ pip install -r requirements/dev.txt

# Pull the postgres docker image
$ docker pull postgres

# Start the DB
$ docker-compose up

# Start the dev server
$ make


```
