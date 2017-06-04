# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from __future__ import absolute_import, unicode_literals
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from reportexport.extensions import db
from reportexport.models import Report


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


def _text_sequence(n):
    with open('tests/data/mock_data.txt', 'r') as data:
        data_str = data.read().strip()

    mock_data = dict(map(lambda row: row.split(' ', 1), data_str.split('\n')))
    idx = 1 + n % len(mock_data)
    return mock_data[str(idx)]


class ReportFactory(BaseFactory):
    """Report factory."""
    id = Sequence(lambda x: x + 1)
    type = Sequence(_text_sequence)

    class Meta:
        """Factory configuration."""

        model = Report
