import json
import pytest
from cStringIO import StringIO

from reportexport.exceptions import AlreadyRegisteredError, InvalidTemplate
from reportexport.templates import Template

from .factories import ReportFactory
from .utils import compare_pdf, PdfNotEqualException


class TestTemplate:
    """Tests for base Template and its helpers."""

    def test_register_new(self):
        class NewTemplate(Template):
            extension = 'new'

            def render(report):
                return ''

        Template.register(NewTemplate)

        assert 'new' in Template._TEMPLATES

        # teardown
        del Template._TEMPLATES['new']

    def test_deregister(self):
        @Template.register
        class NewTemplate(Template):
            extension = 'new'

            def render(report):
                return ''

        assert 'new' in Template._TEMPLATES

        Template.deregister('new')

        assert 'new' not in Template._TEMPLATES

    def test_register_with_same_extension_raises(self):
        pdf_template = Template.get_template('pdf')

        class NewTemplate(Template):
            extension = 'pdf'

            def render(report):
                return ''

        with pytest.raises(AlreadyRegisteredError):
            Template.register(NewTemplate)

        assert Template._TEMPLATES['pdf'] == pdf_template

    def test_template_not_present_raises(self):
        with pytest.raises(InvalidTemplate):
            Template.get_template('invalid-extension')


class TestPdfTemplate:
    """Test suite for PDFTemplate class."""

    def test_render_properly(self, db, report1_pdf):
        ReportFactory.reset_sequence()
        report = ReportFactory()

        res = Template.get_template('pdf').render(report)

        buff = StringIO()
        buff.write(res)

        assert compare_pdf(buff, report1_pdf)

    def test_render_different_with_different_report(self, db, report1_pdf):
        ReportFactory.reset_sequence()
        report = ReportFactory(type='{"organization": "", "reported_at": "", "created_at": "", "inventory": []}')

        res = Template.get_template('pdf').render(report)

        buff = StringIO()
        buff.write(res)

        with pytest.raises(PdfNotEqualException):
            compare_pdf(buff, report1_pdf)

    @pytest.mark.parametrize('missing_param', ['organization', 'reported_at', 'created_at', 'inventory'])
    def test_missing_parameter_raises(self, db, missing_param):
        report_type_dict = {"organization": "", "reported_at": "", "created_at": "", "inventory": []}
        del report_type_dict[missing_param]

        report = ReportFactory(type=json.dumps(report_type_dict))

        with pytest.raises(KeyError):
            Template.get_template('pdf').render(report)

    def test_with_non_model_report(self, report2_pdf):
        """Every object with id and type_dict works the same."""
        from collections import namedtuple

        Report = namedtuple('Report', 'id type_dict')
        report_type_dict = {
            "organization": "Skynet Papercorp",
            "reported_at": "2015-04-22",
            "created_at": "2015-04-23",
            "inventory": [
                {
                    "name": "paper",
                    "price": "4.00"
                }
            ]
        }

        report = Report(2, report_type_dict)
        res = Template.get_template('pdf').render(report)

        buff = StringIO()
        buff.write(res)

        assert compare_pdf(buff, report2_pdf) is True


class TestXMLTemplate:
    """Test suite for XMLTemplate class."""

    def test_render_properly(self, db, report1_xml):
        ReportFactory.reset_sequence()
        report = ReportFactory()

        res = Template.get_template('xml').render(report)

        buff = StringIO()
        buff.write(res)

        assert buff.getvalue() == report1_xml.read().strip()

    def test_render_different_with_different_report(self, db, report1_xml):
        ReportFactory.reset_sequence()
        report = ReportFactory(type='{"organization": "", "reported_at": "", "created_at": "", "inventory": []}')

        res = Template.get_template('xml').render(report)

        buff = StringIO()
        buff.write(res)

        assert buff.getvalue() != report1_xml.read().strip()

    @pytest.mark.parametrize('missing_param', ['organization', 'reported_at', 'created_at', 'inventory'])
    def test_missing_parameter_raises(self, db, missing_param):
        report_type_dict = {"organization": "", "reported_at": "", "created_at": "", "inventory": []}
        del report_type_dict[missing_param]

        report = ReportFactory(type=json.dumps(report_type_dict))

        with pytest.raises(KeyError):
            Template.get_template('xml').render(report)
