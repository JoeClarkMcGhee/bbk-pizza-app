#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.path[0]))
    __package__ = "app"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.pizza.settings")
    execute_from_command_line(sys.argv)
