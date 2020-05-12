import unittest
import app
import re
import json


def get_elem_from_data_html(name_dict, data):
    found_name_dict = re.findall(rf'{name_dict}' + r'="[a-zA-Z0-9_{};:#&\[\]=><,.\- ]*"', data)[0]
    return json.loads(found_name_dict.split(name_dict + '="')[1][0:-1].replace('&#34;', '"'))


class TestFlask(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_default_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        assert 'value="_"' in data   # alphabet
        assert 'value="Q0"' in data  # status_alphabet
        assert set(get_elem_from_data_html('data-ribbon', data).values()) == set('_')
        assert get_elem_from_data_html('data-statuses', data) == ['Q0', ]
        assert get_elem_from_data_html('data-moves', data) == ['=', ]
        assert get_elem_from_data_html('data-change_symbols', data) == ['_', ]

    def test_start(self):
        response = self.app.post('/start', data={
            'alphabet': '_1', 'status_alphabet': 'Q0 Qt',
            'ribbon~0': '_', 'ribbon~1': '_', 'ribbon~-1': '_',
            'input~_~Q0': '1>Qt', 'input~_~Q1': '', 'input~1~Q0': '', 'input~1~Qt': '',
            'pos': 0, 'status': 'Q0', 'steps': 1
        }, follow_redirects=True)
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        assert 'value="_1"' in data      # alphabet
        assert 'value="Q0 Qt"' in data   # status_alphabet
        assert set(get_elem_from_data_html('data-ribbon', data).values()) == {'0', '1', '_'}
        assert get_elem_from_data_html('data-statuses', data) == ['Qt', ]
        assert get_elem_from_data_html('data-moves', data) == ["&gt;", ]    # '&gt;' = '>'
        assert get_elem_from_data_html('data-change_symbols', data) == ['1', ]

    def test_load(self):
        response = self.app.post('/load', data={'save-load': 'add1'}, follow_redirects=True)
        assert response.status_code == 200

        data = response.data.decode('utf-8')
        assert 'value="_01"' in data          # alphabet
        assert 'value="Q0 Q1 Q2 Qt"' in data  # status_alphabet
        assert get_elem_from_data_html('data-ribbon', data)['1'] == '1'
        assert get_elem_from_data_html('data-ribbon', data)['2'] == '0'
        assert get_elem_from_data_html('data-statuses', data) == ['Q0', ]
        assert get_elem_from_data_html('data-moves', data) == ["=", ]
        assert get_elem_from_data_html('data-change_symbols', data) == ['1', ]
