.PHONY: demo build
# actually we do not need to get the old version back for its is stored in the `setup.cfg` file
CURRENT_VERSION=$(shell grep '__version__' scrapy_save_as_pdf/__init__.py |awk '{print $$3}'|awk -F'"' '{print $$2}')
bump_version=\bumpversion --verbose --allow-dirty --commit --tag
# --dry-run
build: release
release:
	pip3 install twine bumpversion
	rm -fr build dist *.egg-info
	python3 setup.py sdist bdist_wheel
	twine check dist/*
test_pypi:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	xdg-open https://test.pypi.org/project/scrapy-save-as-pdf/
pypi:
	twine upload dist/*
	xdg-open https://pypi.org/project/scrapy-save-as-pdf/
test_use:
	pip3 install -i https://test.pypi.org/simple/ scrapy-save-as-pdf -U
use:
	pip3 install -i https://pypi.org/simple/ scrapy-save-as-pdf -U
major:
	${bump_version} major setup.py scrapy_save_as_pdf/__init__.py
	#${bump_version} --current-version ${CURRENT_VERSION} major setup.py scrapy_save_as_pdf/__init__.py
minor:
	${bump_version}  minor setup.py scrapy_save_as_pdf/__init__.py
	#${bump_version}  --current-version ${CURRENT_VERSION} minor setup.py scrapy_save_as_pdf/__init__.py
patch:
	${bump_version}  patch setup.py scrapy_save_as_pdf/__init__.py
	#${bump_version}  --current-version ${CURRENT_VERSION} patch setup.py scrapy_save_as_pdf/__init__.py
demo:
	(cd demo && python3 entry.py)