.PHONY: test lint bench

test:
	./test.py ./spec/*.yml

lint:
	pep8 fett/__init__.py ./setup.py ./test.py ./bench.py
	mypy --strict-optional --disallow-untyped-defs fett/__init__.py

bench:
	python3 -mtimeit -s 'import bench' 'bench.FettBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.JinjaBench.bench()'
	python3 -mtimeit -s 'import bench' 'bench.PystacheBench.bench()'
