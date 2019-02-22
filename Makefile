

help:
	echo build serve
build:
	rm ./docs/* -rf
	mkdir -p ./docs
	cp ./base/static ./docs -r
	cp ./CNAME ./docs/
	python3.5 build.py
upload:
	rsync ./bin/ root@do2:/srv/pymy2/ -r
serve:
	cd ./docs; python3.7 -m http.server
