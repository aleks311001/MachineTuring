from machine_Turing import MachineTuring
import unittest
import json


class TestMT(unittest.TestCase):
    def setUp(self):
        self.mt = MachineTuring()

    def test_new_machine(self):
        data = self.mt.create_dict()
        assert data['alphabet'] == '_'
        assert data['status_alphabet'] == 'Q0'

        program_table = data['program_table']
        assert program_table['line_status'] == ['Q0', ]
        assert program_table['lines']['_']['cells']['Q0'] == ''

        assert json.loads(data['ribbon_cells'])['0'] == '_'
        assert data['pos_start'] == 0
        assert json.loads(data['moves']) == ['=', ]
        assert json.loads(data['change_symbols']) == ['_', ]
        assert json.loads(data['statuses']) == ['Q0', ]

    def test_load(self):
        self.mt.load('simple_test')

        data = self.mt.create_dict()
        assert data['alphabet'] == '_1'
        assert data['status_alphabet'] == 'Q0 Qt'

        program_table = data['program_table']
        assert program_table['line_status'] == ['Q0', 'Qt']
        lines = program_table['lines']
        assert lines['_']['cells']['Q0'] == '1>Qt'
        assert lines['_']['cells']['Qt'] == ''
        assert lines['1']['cells']['Q0'] == ''
        assert lines['1']['cells']['Qt'] == ''

        for ribbon_cell in json.loads(data['ribbon_cells']).values():
            assert ribbon_cell == '_'
        assert data['pos_start'] == 0
        assert json.loads(data['moves']) == ['=', ]
        assert json.loads(data['change_symbols']) == ['_', ]
        assert json.loads(data['statuses']) == ['Q0', ]

    def check_jsons(self, orig_name, test_name):
        with open(f'machines/{orig_name}.json') as original, open(f'machines/{test_name}.json') as test:
            original_mt = json.load(original)
            test_mt = json.load(test)
            assert original_mt['_alphabet'] == test_mt['_alphabet']
            assert original_mt['_status_alphabet'] == test_mt['_status_alphabet']
            assert original_mt['_program_table'] == test_mt['_program_table']

            for i in range(min(original_mt['_ribbon_extremum']['min_index'], test_mt['_ribbon_extremum']['min_index']),
                           max(original_mt['_ribbon_extremum']['max_index'], test_mt['_ribbon_extremum']['max_index'])):
                assert original_mt['_ribbon'].get(str(i), '_') == test_mt['_ribbon'].get(str(i), '_')

            assert original_mt['_pos_ribbon'] == test_mt['_pos_ribbon']
            assert original_mt['_status'] == test_mt['_status']
            assert original_mt['_move'] == test_mt['_move']

    def test_save(self):
        self.mt.load('simple_test')
        self.mt.save('tests/test_save')

        self.check_jsons('simple_test', 'tests/test_save')

    def test_next_step(self):
        self.mt.load('simple_test')
        self.mt.next_step()
        self.mt.save('tests/next_step_simple_test')
        self.check_jsons('tests/check_next_step_simple_test', 'tests/next_step_simple_test')

        self.mt.load('hard_test')
        self.mt.next_step()
        self.mt.save('tests/next_step_hard_test')
        self.check_jsons('tests/check_next_step_hard_test', 'tests/next_step_hard_test')

    def test_start(self):
        self.mt.load('hard_test')
        self.mt.start(25)
        self.mt.save('tests/start_hard_test')
        self.check_jsons('tests/check_start_hard_test', 'tests/start_hard_test')

        self.mt.load('long_test')
        self.mt.start(250)
        self.mt.save('tests/start_long_test')
        self.check_jsons('tests/check_start_long_test', 'tests/start_long_test')
