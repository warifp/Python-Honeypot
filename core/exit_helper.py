#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ctypes
from core.alert import error
from core.alert import info
from core.color import finish


def exit_success():
    """
    exit the framework with code 0
    """
    finish()
    sys.exit(0)


def exit_failure(msg):
    """
    exit the framework with code 1

    Args:
        msg: the error message
    """

    error(msg)
    finish()
    sys.exit(1)


def terminate_thread(thread, output=True):
    """
    kill a thread https://stackoverflow.com/a/15274929

    Args:
        thread: an alive thread
        output: print while killing

    Returns:
        True/None
    """
    if output:
        info("killing {0}".format(thread.name))
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident),
        exc
    )
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    return True