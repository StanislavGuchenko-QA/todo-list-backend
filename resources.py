import json
import os.path


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')

class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_json(cls, grocery_list):
        new_entry = cls(grocery_list['title'])
        for sub_entry in grocery_list.get('entries', []):
            new_entry.add_entry(cls.from_json(sub_entry))
        return new_entry

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        filename = os.path.join(path, f"{self.title}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.json(), f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_json(data)

    def __str__(self):
        return self.title


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title):
        self.entries.append(Entry(title))

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)