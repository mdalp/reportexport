from cStringIO import StringIO

from .factories import ReportFactory
from .utils import compare_pdf, PdfNotEqualException


class TestReport:
    """Tests for report views."""

    def test_invalid_report_format(self, testapp, db):
        res = testapp.get('/report/report-1.txt')

        assert res.status_code == 404
        assert 'Report not available in &quot;txt&quot; format. Formats available: [\'xml\', \'pdf\']' in res.data

    def test_invalid_report_id_404(self, testapp, db):
        """A request for a not existing id returns 404."""
        res = testapp.get('/report/report-1.xml')

        assert res.status_code == 404
        assert 'Report with id &quot;1&quot; does not exist.' in res.data

    def test_valid_report_id(self, testapp, db):
        """Test a request for a report with a valid report_id and extension returns 200."""
        ReportFactory.reset_sequence()
        ReportFactory()

        res = testapp.get('/report/report-1.xml')

        assert res.status_code == 200

    def test_correct_xml_data(self, testapp, db, report1_xml):
        """Test xml generated is what expected."""
        ReportFactory.reset_sequence()
        ReportFactory()

        res = testapp.get('/report/report-1.xml')

        assert res.status_code == 200

        assert res.data == report1_xml.read().strip()

    def test_correct_pdf_data(self, testapp, db, report1_pdf):
        """Test pdf generated is what expected."""
        ReportFactory.reset_sequence()
        ReportFactory()

        res = testapp.get('/report/report-1.pdf')

        assert res.status_code == 200

        # with open('tests/data/report-1.pdf', 'rb') as expected_data:
        buff = StringIO()
        buff.write(res.data)

        try:
            assert compare_pdf(buff, report1_pdf) is True
        except PdfNotEqualException:
            with open('tests/data/test-result_report-1.pdf', 'w+') as f:
                f.write(res.data)
            raise


class TestHealthCheck:
    def test_success(self, testapp):
        res = testapp.get('/report/healthcheck')

        assert res.status_code == 200
        assert res.data == 'OK'