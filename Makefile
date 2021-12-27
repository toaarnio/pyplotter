deps:
	pip3 install -r requirements.txt

lint:
	prospector pyplottr/*

test:
	python3 setup.py test
	python3 pyplottr/pyplottr.py
	python3 sample.py

install:
	pip3 uninstall --yes pyplottr || true
	rm -rf build dist pyplottr.egg-info || true
	python3 setup.py sdist bdist_wheel
	pip3 install --user dist/*.whl
	@python3 -c 'import pyplottr; print(f"Installed pyplottr version {pyplottr.__version__}.")'

release:
	pip3 install --user setuptools wheel twine
	make install
	twine upload dist/*

.PHONY: deps lint test install release
