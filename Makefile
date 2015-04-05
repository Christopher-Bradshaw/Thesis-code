.PHONY: test clean

test: clean
	python3 -m unittest discover -v -s test

clean:
	rm *.pyc test/*.pyc helpers/*.pyc standalone_scripts/*.pyc 2>/dev/null || true
