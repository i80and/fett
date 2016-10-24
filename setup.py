#!/usr/bin/env python
import sys
from distutils.command.build_py import build_py as _build_py
from setuptools import setup


class BuildPy27(_build_py):
    """A custom builder that translates Python 3 source into Python 2."""
    FIXERS = ('absimport', 'annotations', 'bitlength', 'bool', 'bytes',
              'classdecorator', 'collections', 'dctsetcomp', 'division',
              'except', 'features', 'fullargspec', 'funcattrs', 'getcwd',
              'imports', 'imports2', 'input', 'int', 'intern', 'itertools',
              'kwargs', 'memoryview', 'metaclass', 'methodattrs', 'newstyle',
              'next', 'numliterals', 'open', 'printfunction', 'raise',
              'range', 'reduce', 'setliteral', 'str', 'super', 'throw', 'with',
              'unpacking', 'unittest')

    def __init__(self, *args, **kwargs):
        _build_py.__init__(self, *args, **kwargs)
        import logging
        from lib2to3 import refactor
        import lib3to2.main

        rt_logger = logging.getLogger('RefactoringTool')
        rt_logger.addHandler(logging.StreamHandler())
        self.rtool = lib3to2.main.StdoutRefactoringTool(
            ['lib3to2.fixes.fix_{}'.format(s) for s in self.FIXERS],
            None,
            [],
            False,
            False
        )

    def copy_file(self, source, target, **_):
        if not source.endswith('.py'):
            return

        try:
            print('3to2 converting: %s => %s' % (source, target))
            with open(source, 'rt') as input_file:
                # ensure file contents have trailing newline
                source_content = input_file.read() + '\n'
                nval = self.rtool.refactor_string(source_content, source)

            if nval is not None:
                # The intern() argument must be unicode in Py3 and bytes in Py2
                nval = str(nval).replace('intern(u\'', 'intern(\'')

                with open(target, 'wt') as output:
                    output.write('from __future__ import print_function\n')
                    output.write(nval)
            else:
                raise ValueError('Failed to parse: %s' % source)
        except (ValueError, IOError) as err:
            print('3to2 error (%s => %s): %s' % (source, target, err))

VERSION = '0.1.0'

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python',
    'Topic :: Text Processing :: Markup'
)

SETUP_REQUIRES = []
INSTALL_REQUIRES = []

CMDCLASS = {}
if sys.version_info[0] < 3:
    SETUP_REQUIRES.append('3to2')
    CMDCLASS['build_py'] = BuildPy27

if sys.version_info < (3, 5, 0):
    INSTALL_REQUIRES.append('typing')

if __name__ == '__main__':
    setup(name='fett',
          version=VERSION,
          license='MIT',
          description='A fast indentation-preserving template engine.',
          long_description=open('README.rst').read(),
          author='Andrew Aldridge',
          author_email='i80and@foxquill.com',
          url='https://github.com/i80and/fett',
          setup_requires=SETUP_REQUIRES,
          install_requires=INSTALL_REQUIRES,
          classifiers=CLASSIFIERS,
          cmdclass=CMDCLASS,
          package_dir={'fett': 'fett'},
          packages=['fett'])
