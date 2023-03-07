install:
	$(MAKE) -C analysis install

test:
	$(MAKE) -C analysis test

lint:
	$(MAKE) -C analysis lint

doc:
	$(MAKE) -C analysis doc
