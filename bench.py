#!/usr/bin/env python3
import timeit
import fett
import jinja2
import pystache


class FettBench:
    template = fett.Template('''{{ for step in steps }}
.. only:: not (html or dirhtml or singlehtml)

   Step {{ i inc }}: {{ step.title }}
   {{ heading }}

   {{step.body}}

.. only:: html or dirhtml or singlehtml

   .. raw:: html

      <div class="sequence-block">
        <div class="bullet-block">
          <div class="sequence-step">{{i inc}}</div></div>

   {{step.title}}
   {{heading}}

   {{step.body}}

   .. raw:: html

      </div>
{{ end }}''')

    @classmethod
    def bench(cls):
        cls.template.render(DATA)


class JinjaBench:
    template = jinja2.Template('''   {% for step in steps %}
.. only:: not (html or dirhtml or singlehtml)

   Step {{ loop.index }}: {{ step.title }}
   {{ heading }}

   {{step.body|indent(3)}}

.. only:: html or dirhtml or singlehtml

   .. raw:: html

      <div class="sequence-block">
        <div class="bullet-block">
          <div class="sequence-step">{{loop.index}}</div></div>

   {{step.title}}
   {{heading}}

   {{step.body|indent(3)}}

   .. raw:: html

      </div>
{% endfor %}''')

    @classmethod
    def bench(cls):
        cls.template.render(DATA)


class PystacheBench:
    template = pystache.parse('''
{{ #steps }}
.. only:: not (html or dirhtml or singlehtml)

   Step 0: {{ title }}
   {{ heading }}

   {{body}}

.. only:: html or dirhtml or singlehtml

   .. raw:: html

      <div class="sequence-block">
        <div class="bullet-block">
          <div class="sequence-step">0</div></div>

   {{title}}
   {{heading}}

   {{body}}

   .. raw:: html

      </div>
{{/steps}}
''')

    @classmethod
    def bench(cls):
        pystache.render(cls.template, DATA)

DATA = {
    'heading': '~~~~~~~~~~~~~~~~~~~~~',
    'steps': [
        {'title': 'Install', 'body': 'Do things\n\n- Thing1\n-Thing 2\n\n'},
        {'title': 'Use', 'body': 'Use'},
        {'title': 'Finish', 'body': 'Finish up'},
    ]}
