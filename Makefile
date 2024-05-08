.PHONY: clean format test

clean:
	rm -rf *.so deflate.egg-info build

format:
	clang-format -i deflate.c
	ruff check
	ruff format

test: clean
	pip install -e .[test]
	pytest
