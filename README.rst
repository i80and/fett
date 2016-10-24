.. |travis| image:: https://travis-ci.org/i80and/fett.svg?branch=master
            :target: https://travis-ci.org/i80and/fett

=============
Fett |travis|
=============

Overview
--------

Example
-------

.. code-block:: python

   import fett

   fett.Template('''{{ for customer in customers }}
   {{ if i even }}
   Even: {{ customer.name }}
   {{ else }}
   Odd: {{ customer.name }}
   {{ end }}
   {{ else }}
   No customers :(
   {{ end }}''').render({'customers': [
       {'name': 'Bob'},
       {'name': 'Elvis'},
       {'name': 'Judy'}
   ]})

Syntax
------

==========================================   ===========
Tag Format                                   Description
==========================================   ===========
``{{ <expression> }}``                       `Substitution <subsblock>`_
``{{ if <expression> }}``                    `Conditional <ifblock>`_
``{{ for <expression> in <expression> }}``   `Loop <forblock>`_
``{{ else }}``
``{{ end }}``                                Block termination
``{{ # <comment> }}``                        `Comment <comment>`_
==========================================   ===========

Spaces between tag opening/closing delimiters are optional.

Expressions
~~~~~~~~~~~

An **expression** is given for `substitutions <subsblock>`,
`conditionals <ifblock>`, and `loops <forblock>`.

Expressions take the following form:

``<name>[.<subfield>...] [<filter> [<filter2>...]]``

.. _subsblock:

Substitutions
~~~~~~~~~~~~~

.. _ifblock:

Conditionals
~~~~~~~~~~~~

.. _forblock:

Loops
~~~~~

.. _comment:

Comments
~~~~~~~~
