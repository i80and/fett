#!/usr/bin/env python
import sys
import fett
import yaml


def main(args):
    paths = args[1:]
    for path in paths:
        with open(path, 'r') as f:
            data = yaml.load(f)

        for test in data['tests']:
            name = test['name']
            template = test['template']
            expected = test['expected']
            data = test['data']

            print(path, name)
            compiled = fett.Template(template)
            rendered = compiled.render(data)

            try:
                assert rendered == expected
            except AssertionError as err:
                print('Got:      ', repr(rendered))
                print('Expected: ', repr(expected))
                raise err

if __name__ == '__main__':
    main(sys.argv)
