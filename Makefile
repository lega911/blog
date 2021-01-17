

help:
	echo build serve
build:
	rm ./docs/* -rf
	mkdir -p ./docs
	cp ./base/static ./docs -r
	cp ./CNAME ./docs/
	python3 build.py
serve:
	cd ./docs; python3 -m http.server
