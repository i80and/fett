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
``{{ <expression> }}``                       Substitutions_
``{{ format <name> }}``                      Metaformatting_
``{{ if <expression> }}``                    Conditionals_
``{{ for <name> in <expression> }}``         Loops_
``{{ else }}``
``{{ end }}``                                Block termination
``{{ # <comment> }}``                        Comments_
==========================================   ===========

Spaces between tag opening/closing delimiters are optional.

Expressions
~~~~~~~~~~~

An **expression** is given for Substitutions_, Conditionals_, and Loops_.

Expressions take the following form:

``<name>[.<subfield>...] [<filter> [<filter2>...]]``

You can use **filters** to modify a single value in simple ways. For example,
the loop iteration counter ``i`` counts from ``0``, but users often wish to
count from ``1``. You can obtain a count-from-1 value with the expression
``i inc``.

The full list of available filters follows.

===========  ======
Filter Name  Effect
===========  ======
car          Returns the first element of a list.
cdr          Returns all but the first element of a list.
dec          Decrements a value representable as an integer by one.
even         Returns true iff its input is representable as an even integer.
inc          Increments a value representable as an integer by one.
len          Returns the length of a list.
not          Returns the inverse of a boolean.
odd          Returns true iff its input is representable as an odd integer.
negative     Returns true iff its input is representable as an integer < 0.
positive     Returns true iff its input is representable as an integer > 0.
split        Splits a value into a list by whitespace.
strip        Returns the input string with surrounding whitespace removed.
timesNegOne  Returns int(input) * -1
zero         Returns true iff the input is zero
===========  ======

Substitutions
~~~~~~~~~~~~~

Metaformatting
~~~~~~~~~~~~~~

Conditionals
~~~~~~~~~~~~

Loops
~~~~~

Comments
~~~~~~~~
