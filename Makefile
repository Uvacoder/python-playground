MAKEFLAGS+="-j 2"

.PHONY: all
all: dev

dev-server:
	uvicorn main:app --reload

dev-client:
	npm run --prefix web dev

dev: dev-server dev-client