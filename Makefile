CURRENT_VERSION=$(shell grep '__version__' scrapy_save_as_pdf/__init__.py |awk '{print $$3}'|awk -F'"' '{print $$2}')
bump_version=\bumpversion --verbose
# --allow-dirty
# --dry-run
release:
	pip3 install twine bumpversion
	python3 setup.py sdist bdist_wheel
	twine check dist/*
test_pypi:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	xdg-open https://test.pypi.org/project/scrapy-save-as-pdf/
pypi:
	twine upload dist/*
	xdg-open https://pypi.org/project/scrapy-save-as-pdf/
test_use:
	pip install -i https://test.pypi.org/simple/ scrapy-save-as-pdf
use:
	pip install scrapy-save-as-pdf
major:
	${bump_version} --current-version $(CURRENT_VERSION) major setup.py scrapy_save_as_pdf/__init__.py
minor:
	${bump_version}  --current-version ${CURRENT_VERSION} minor setup.py scrapy_save_as_pdf/__init__.py
patch:
	${bump_version}  --current-version ${CURRENT_VERSION} patch setup.py scrapy_save_as_pdf/__init__.py