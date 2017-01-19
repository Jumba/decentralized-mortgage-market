.PHONY: all test clean

all: clean test

test: 
	nosetests --with-coverage --cover-package=market --cover-xml --cover-inclusive --cover-xml-file=coverage.xml --cover-html --cover-html-dir=html_coverage test/market
	xdg-open html_coverage/index.html

clean:
	rm -rf html_coverage dispersy_temp* *.db test/dispersy_temp* test/market/*.db .coverage
