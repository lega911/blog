

help:
	echo build serve
build:
	rm ./bin/* -rf
	mkdir -p ./bin
	cp ./base/static ./bin -r
	python3.5 build.py
upload:
	rsync ./bin/ root@do2:/srv/pymy2/ -r
serve:
	cd ./bin; python3.6 -m http.server
