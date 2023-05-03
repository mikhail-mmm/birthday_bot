ifneq (,$(wildcard .env))
	$(info Found .env file.)
	include .env
	export
endif

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

style:
	fleke8 track

types:
	mypy track

check:
	make -j2 style types

test:
	PYTHONPATH=. pytest