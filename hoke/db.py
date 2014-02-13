import datetime
import json
import os

from . import data


def new_db(data_path):
    return Db(open(data_path, 'wb+'))


def open_db(data_path):
    return Db(open(data_path, 'rb+'))


class Db(object):
    def __init__(self, fd):
        self.fd = fd

    def add_blueprint(self, raw_bp):
        self.fd.seek(0, os.SEEK_END)
        row = {}
        for name, value in zip(raw_bp._fields, raw_bp):
            if name.startswith('date') and value is not None:
                value = {
                    'type': 'datetime',
                    'value': [value.year, value.month, value.day, value.hour,
                              value.minute, value.second, value.microsecond],
                }
            row[name] = value
        self.fd.write(json.dumps(row))
        self.fd.write('\n')

    def list_blueprints(self):
        self.fd.seek(0)
        for line in self.fd:
            row = json.loads(line)
            for key in row.keys():
                value = row[key]
                if key.startswith('date') and value is not None:
                    assert value['type'] == 'datetime'
                    row[key] = datetime.datetime(*value['value'])
            yield data.RawBlueprint(**row)

    def close(self):
        self.fd.close()
        self.fd = None
