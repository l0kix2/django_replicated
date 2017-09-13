# coding: utf-8
from __future__ import unicode_literals

from django import db
import datetime
import functools
import logging

log = logging.getLogger(__name__)


def get_object_name(obj):
    try:
        return obj.__name__
    except AttributeError:
        return obj.__class__.__name__


class Routers(object):
    def __getattr__(self, name):
        for r in db.router.routers:
            if hasattr(r, name):
                return getattr(r, name)
        msg = 'Not found the router with the method "%s".' % name
        raise AttributeError(msg)


routers = Routers()


def timeit(marker=None):
    def decorator(func):
        name = marker or func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            before = datetime.datetime.now()
            msg = '%s executed in %d.%06d'
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                msg += ' with exception %s %s' % (exc.__class__.__name__, exc)
            finally:
                passed = datetime.datetime.now() - before
                logging.debug(msg, name, passed.seconds, passed.microseconds)
        return wrapped
    return decorator
