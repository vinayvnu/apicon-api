install:
	# install files
	pip install --upgrade pip
	pip install -r requirements.txt

format:
	black app/*.py app/routers/*.py

lint:
	# it disables Recommended warnings(R) and configuration warnings(C)
	pylint --disable=R,C app/*.py app/routers/*.py

freeze:
	pip freeze >requirements.txt

#test:
#	python -m pytest -vv --cov=mylib test_logic.py

#build:
#        docker build -t deploy-fatapi .
#
#run:
#        docker run -p 127.0.0.1:8080:8080 c5b9a186a163