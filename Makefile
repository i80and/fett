PYTHON:=`which python`
.PHONY: test lint bench

test:
	cd spec && $(PYTHON) ./test.py ./*.yml

lint:
	pep8 fett/__init__.py ./setup.py ./bench.py ./spec/test.py
	mypy --strict-optional --disallow-untyped-defs fett/__init__.py

bench:
	python3 -mtimeit -s 'import bench' 'bench.FettBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.JinjaBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.PystacheBench.bench()'
