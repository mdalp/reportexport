# -*- coding: utf-8 -*-
"""Fixtures to help in tests."""
from __future__ import absolute_import, unicode_literals
import pytest

from reportexport.app import create_app
from reportexport.extensions import db as _db
from reportexport.settings import TestConfig


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A test app."""
    return app.test_client()


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.yield_fixture(scope='function')
def report1_pdf():
    with open('tests/data/report-1.pdf', 'rb') as expected_data:
        yield expected_data

@pytest.yield_fixture(scope='function')
def report2_pdf():
    with open('tests/data/report-2.pdf', 'rb') as expected_data:
        yield expected_data


@pytest.yield_fixture(scope='function')
def report1_xml():
    with open('tests/data/report-1.xml', 'rb') as expected_data:
        yield expected_data


@pytest.yield_fixture(scope='function')
def report2_xml():
    with open('tests/data/report-2.xml', 'rb') as expected_data:
        yield expected_data
