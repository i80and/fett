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
            expected = test.get('expected', None)
            data = test['data']

            print(path, name)

            try:
                compiled = fett.Template(template)
                rendered = compiled.render(data)
            except (ValueError, TypeError) as err:
                if not test.get('error', False):
                    raise err  # pragma: no cover

                continue

            try:
                assert rendered == expected
            except AssertionError as err:  # pragma: no cover
                print('Got:      ', repr(rendered))
                print('Expected: ', repr(expected))
                raise err

if __name__ == '__main__':
    main(sys.argv)
