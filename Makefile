

help:
	echo build
build:
	rm ./bin/ -rf
	mkdir ./bin
	cp ./base/static ./bin -r
	python3.5 build.py
upload:
	rsync ./bin/ root@do2:/srv/pymy2/ -r
