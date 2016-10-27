PYTHON:=`which python`
.PHONY: test lint bench

test-travis:
	cd spec && $(PYTHON) ./test.py ./*.yml

test:
	PYTHONPATH=. python3 ./spec/test.py ./spec/*.yml

coverage:
	PYTHONPATH=. coverage run ./spec/test.py ./spec/*.yml
	coverage report --omit=renderer

lint:
	pep8 fett/__init__.py ./setup.py ./bench.py ./spec/test.py
	mypy --strict-optional --disallow-untyped-defs fett/__init__.py

bench:
	PYTHONPATH=. python3 -mtimeit -s 'import bench' 'bench.FettBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.JinjaBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.PystacheBench.bench()'
