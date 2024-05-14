all: run

run:
	python3 main.py

clean:
	rm -r __pycache__ Model/__pycache__