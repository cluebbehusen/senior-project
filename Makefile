setup:
	pip3 install -r requirements.txt

test:
	python3 -m unittest discover -s tests
