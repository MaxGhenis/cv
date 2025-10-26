.PHONY: help install test build html pdf clean watch

help:
	@echo "CV Build Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make build      - Build HTML and PDF"
	@echo "  make html       - Build HTML only"
	@echo "  make pdf        - Build PDF only"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make all        - Install, test, and build"

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

test:
	. venv/bin/activate && pytest test_cv.py -v

build:
	. venv/bin/activate && python build.py

html:
	. venv/bin/activate && python build.py --html

pdf:
	. venv/bin/activate && python build.py --pdf

clean:
	rm -f cv.html cv.pdf cv_test.pdf
	rm -rf __pycache__ .pytest_cache

all: install test build

# Run tests on file changes (requires: pip install pytest-watch)
watch:
	. venv/bin/activate && ptw -- test_cv.py -v
