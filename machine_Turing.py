import math

from flask import Flask, jsonify, request, redirect, send_from_directory, render_template
from dataclasses import dataclass
import json
import re

@dataclass
class Cell:
    input_text: str = ''
    output_text: str = ''
    execution_count: int = 0


class MachineTuring:
    _HTML_TEMPLATE_PATH = "machine.html"

    def __init__(self):
        self._alphabet = '_'
        self._status_alphabet = ['Q0', ]
        self._program_table = {'_': {'Q0': ''}}
        self._ribbon = {'0': '_'}
        self._ribbon_extremum = {'min_index': 0, 'max_index': 0}
        self._status = 'Q0'
        self._pos_ribbon = 0
        self._move = '='

        self._moves = [self._move, ]
        self._pos_start = self._pos_ribbon
        self._change_symbols = [self._ribbon[str(self._pos_start)], ]
        self._statuses = [self._status, ]
        self._before_ribbon = self._ribbon

    def clear(self):
        self.__init__()

    def clear_story(self):
        self._moves = ["=", ]
        self._pos_start = self._pos_ribbon
        self._change_symbols = [self._ribbon[str(self._pos_start)], ]
        self._statuses = [self._status, ]
        self._before_ribbon = self._ribbon

    def create_dict(self):
        result = dict(alphabet=self._alphabet, status_alphabet=' '.join(self._status_alphabet),
                      program_table=self.make_program_table(), ribbon_cells=json.dumps(self._before_ribbon),
                      ribbon_extremum=json.dumps(self._ribbon_extremum),
                      pos_start=self._pos_start, moves=json.dumps(self._moves),
                      change_symbols=json.dumps(self._change_symbols), statuses=json.dumps(self._statuses))

        self.clear_story()
        return result

    def render(self):
        return render_template(self._HTML_TEMPLATE_PATH, **self.create_dict())

    def make_program_table(self):
        result = dict()
        result['line_status'] = self._status_alphabet

        result['lines'] = dict()
        for symbol in self._alphabet:
            line = dict()

            line['symbol'] = symbol
            if symbol == ' ':
                line['symbol'] = '˽'

            line['cells'] = dict()
            for status in self._status_alphabet:
                line['cells'][status] = self._program_table[symbol][status]
            line['index_cells'] = self._status_alphabet

            result['lines'][symbol] = line

        result['index_lines'] = self._alphabet

        return result

    def update_alphabet(self):
        new_alphabet = request.form.get('alphabet')

        for symbol in set(new_alphabet) ^ set(self._alphabet):
            if symbol not in self._program_table:
                self._program_table[symbol] = dict()
                for status in self._status_alphabet:
                    self._program_table[symbol][status] = ''
            else:
                self._program_table.pop(symbol)

        self._alphabet = new_alphabet

    def update_status_alphabet(self):
        new_status_alphabet = str(request.form.get('status_alphabet')).split(' ')

        for symbol in self._program_table:
            for status in set(new_status_alphabet) ^ set(self._status_alphabet):
                if status in self._status_alphabet:
                    self._program_table[symbol].pop(status)
                else:
                    self._program_table[symbol][status] = ''

        self._status_alphabet = new_status_alphabet

    def load_program_table_and_ribbon(self):
        self._status = request.form.get('status')
        self._pos_ribbon = int(request.form.get('pos'))

        for item in request.form:
            name = item.split('~')
            if name[0] == 'ribbon':
                index = name[1]
                self._ribbon[index] = request.form.get(item)
            elif name[0] == 'input':
                self._program_table[name[1]][name[2]] = request.form.get(item)

        self._ribbon_extremum['min_index'] = min(int(i) for i in self._ribbon.keys())
        self._ribbon_extremum['max_index'] = max(int(i) for i in self._ribbon.keys())

    def update_all(self):
        self.update_alphabet()
        self.update_status_alphabet()
        self.load_program_table_and_ribbon()
        self.clear_story()

    def start(self, steps):
        self._before_ribbon = self._ribbon.copy()
        self._moves = list()
        self._pos_start = self._pos_ribbon
        self._change_symbols = list()
        self._statuses = list()

        last_pos = self._pos_ribbon
        step = 0
        while step < steps and self.next_step():
            self._moves.append(self._move)
            self._change_symbols.append(self._ribbon[str(last_pos)])
            self._statuses.append(self._status)
            last_pos = self._pos_ribbon
            step += 1

    def next_step(self):
        program = self._program_table[self._ribbon[str(self._pos_ribbon)] or ' '][self._status]
        move = re.findall(r'[<=>]', program)
        if len(move) == 0:
            return False
        else:
            self._move = move[0]

        self._ribbon[str(self._pos_ribbon)] = program.split(self._move)[0]
        self._status = program.split(self._move)[1]

        self.check_not_extremum_cell()

        if self._status not in self._status_alphabet or self._ribbon[str(self._pos_ribbon)] not in self._alphabet:
            return False

        if self._move == '<':
            self._pos_ribbon -= 1
        elif self._move == '>':
            self._pos_ribbon += 1

        return True

    def check_not_extremum_cell(self):
        if self._pos_ribbon == self._ribbon_extremum['max_index']:
            self._ribbon_extremum['max_index'] += 1
            self._ribbon[str(self._ribbon_extremum['max_index'])] = '_'
        if self._pos_ribbon == self._ribbon_extremum['min_index']:
            self._ribbon_extremum['min_index'] -= 1
            self._ribbon[str(self._ribbon_extremum['min_index'])] = '_'

    def save(self, name):
        filename = 'machines/' + name + '.json'

        with open(filename, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    def load(self, name):
        filename = 'machines/' + name + '.json'

        with open(filename, 'r') as file:
            machine = dict(json.load(file))

        for key in machine.keys():
            self.__setattr__(key, machine[key])
