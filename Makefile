.PHONY: clean build upload

clean:
	rm -rf build dist *.egg-info

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

all: clean build upload