.PHONY: ci

ci:
	act workflow_dispatch \
		--container-architecture linux/amd64 \
		--directory . \
		-P ubuntu-latest=catthehacker/ubuntu:act-latest
