# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import commands

from tests.asserts import assert_equals
from lettuce.fs import FileSystem

current_directory = FileSystem.dirname(__file__)
lib_directory = FileSystem.join(current_directory,  'lib')


OLD_PYTHONPATH = os.getenv('PYTHONPATH', ':'.join(sys.path))


def teardown():
    os.environ['PYTHONPATH'] = OLD_PYTHONPATH


def test_django_admin_media_serving_on_django_13():
    'lettuce should serve admin static files properly on Django 1.3'

    os.environ['PYTHONPATH'] = "%s:%s" % (
        FileSystem.join(lib_directory, 'Django-1.3'),
        OLD_PYTHONPATH,
    )

    FileSystem.pushd(current_directory, "django", "grocery")

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=2 ./features/")

    assert_equals(status, 0, out)
    FileSystem.popd()

    lines = out.splitlines()

    assert u"Preparing to serve django's admin site static files..." in lines
    assert u'Running on port 7000 ... OK' in lines
    assert u'Fetching admin media ... OK' in lines
    assert u'Fetching static files ... OK' in lines
    assert u'Fetching CSS files: ... OK' in lines
    assert u'Fetching javascript files: ... OK' in lines
    assert u"Django's builtin server is running at 0.0.0.0:7000" in lines


def test_django_admin_media_serving_on_django_125():
    'lettuce should serve admin static files properly on Django 1.2.5'

    os.environ['PYTHONPATH'] = "%s:%s" % (
        FileSystem.join(lib_directory, 'Django-1.2.5'),
        OLD_PYTHONPATH,
    )
    FileSystem.pushd(current_directory, "django", "grocery")

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=2 ./features/")

    assert_equals(status, 0, out)
    FileSystem.popd()

    lines = out.splitlines()
    failure = '\n\n'
    failure += '*' * 100
    failure += '\n' + '\n'.join(lines)

    assert u"Preparing to serve django's admin site static files..." in lines, failure
    assert u"Django's builtin server is running at 0.0.0.0:7000" in lines, failure
    assert u'Running on port 7000 ... OK' in lines, failure
    assert u'Fetching admin media ... OK' in lines, failure
    assert u'Fetching static files ... OK' in lines, failure
    assert u'Fetching CSS files: ... OK' in lines, failure
    assert u'Fetching javascript files: ... OK' in lines, failure
