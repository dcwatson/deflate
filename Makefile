.PHONY: clean format test

clean:
	rm -rf *.so deflate.egg-info build

format:
	clang-format -i deflate.c
	black tests
	isort tests

test: clean
	pip install -e .
	pytest
