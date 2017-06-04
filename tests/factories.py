# -*- coding: utf-8 -*-
"""Factories to help in tests."""
import json
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
    mock_data = json.load(open('tests/data/mock_data.json', 'r'))
    idx = 1 + n % len(mock_data)
    return json.dumps(mock_data[str(idx)])


class ReportFactory(BaseFactory):
    """Report factory."""
    id = Sequence(lambda x: x + 1)
    type = Sequence(_text_sequence)

    class Meta:
        """Factory configuration."""

        model = Report
