
all:
	echo

bump-upload:
	$(MAKE) bump
	$(MAKE) upload

docs:

test:
	python -c "from aido_agents import *"
	nosetests aido_agents_tests

bump: # v2
	bumpversion patch
	git push --tags
	git push


upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload --skip-existing --verbose dist/*


black:
	black -l 110 src setup.py
