from __future__ import absolute_import, unicode_literals
import pytest

from reportexport.models import Report

from .factories import ReportFactory

expected_type_mock = {
    1: '{"reported_at": "2015-04-21", "organization": "Dunder Mifflin", "created_at": "2015-04-22", "inventory": [{"price": "2.00", "name": "paper"}, {"price": "5.00", "name": "stapler"}, {"price": "125.00", "name": "printer"}, {"price": "3000.00", "name": "ink"}]}',
    2: '{"reported_at": "2015-04-22", "organization": "Skynet Papercorp", "created_at": "2015-04-23", "inventory": [{"price": "4.00", "name": "paper"}]}',
}


class TestReportFactory:
    """Tests for ReportFactory"""

    def test_generates_correct_data_and_populate_db(self, db):
        ReportFactory.reset_sequence()
        report = ReportFactory()

        assert report.id == 1
        assert report.type == expected_type_mock[1]

        queried_report = Report.query.first()

        assert queried_report.id == 1
        assert queried_report.type == expected_type_mock[1]

    def test_generates_correct_data(self, db):
        ReportFactory.reset_sequence()
        report = ReportFactory()

        assert report.id == 1
        assert report.type == expected_type_mock[1]

    @pytest.mark.parametrize('n_reports,expected_type_mock_list', [
        (1, (1,)),
        (2, (1, 2)),
        (3, (1, 2, 1)),
        (4, (1, 2, 1, 2)),
        (8, (1, 2, 1, 2, 1, 2, 1, 2)),
    ])
    def test_generates_correct_data_called_multiple_times(self, db, n_reports, expected_type_mock_list):
        ReportFactory.reset_sequence()
        reports = ReportFactory.create_batch(n_reports)

        for report, mock_id in zip(reports, expected_type_mock_list):
            assert report.type_dict == expected_type_mock[mock_id]
