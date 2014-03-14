from dashboard.url_to_info import UrlToInfo
from mock import patch


def test_search_should_not_return_info():
    u = UrlToInfo()
    assert u.lookup('search?q=foo') is None


def test_entrance_should_not_return_info():
    u = UrlToInfo()
    assert u.lookup('(entrance)') is None


def test_normalise_path_smart_answer_root():
    assert UrlToInfo.normalise_path('/overseas-passports') == '/overseas-passports'

def test_normalise_path_smart_answer_1_level():
    assert UrlToInfo.normalise_path('/overseas-passports/y') == '/overseas-passports'

def test_normalise_path_smart_answer_2_level():
    assert UrlToInfo.normalise_path('/overseas-passports/y/foo') == '/overseas-passports'

def test_transaction_url_to_info():
    with patch('dashboard.url_to_info.UrlToInfo.fetch_content') as fc_mock:
        fc_mock.return_value.content = '''
<script id="ga-params" type="text/javascript">
GOVUK.Analytics.Proposition = "citizen";
_gaq.push(["_setCustomVar",2,"Format","transaction",3]);
GOVUK.Analytics.Format = "transaction";</script>
'''
        u = UrlToInfo()
        assert u.lookup('/apply-blue-badge') == {
            'format': 'transaction',
        }


def test_org_url_to_info():
    with patch('dashboard.url_to_info.UrlToInfo.fetch_content') as fc_mock:
        fc_mock.return_value.content = '''
<script id="ga-params" type="text/javascript">
_gaq.push(["_setCustomVar",9,"Organisations","<EA74>",3]);
GOVUK.Analytics.Organisations = "<EA74>";</script>
'''
        u = UrlToInfo()
        assert u.lookup('/government/organisations/driver-and-vehicle-licensing-agency') == {
            'orgs': ['EA74'],
        }
