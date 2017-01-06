# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = build
PYTHON        = python2

# Internal variables.
ALLSPHINXOPTS   = -d .doctrees $(SPHINXOPTS) .

.PHONY: clean html deploy

html:
	$(PYTHON) npc/update-npc.py
	$(PYTHON) update-fits.py
	$(PYTHON) wallet.py && cp srp.json $(BUILDDIR)/
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/
	touch $(BUILDDIR)/.nojekyll
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/"

submodule:
	[ -e $(BUILDDIR)/.git ] || git submodule init && git submodule update

clean:
	cd $(BUILDDIR) && git fetch && git reset --hard origin/master
	-rm -rf $(BUILDDIR)/*
	-rm -rf .doctrees

deploy: clean html
	lockfile-create --retry 1 deploy
	cd $(BUILDDIR) && \
		git add -A && \
		git commit -m "Updated at `LANG=C date`" && \
		git push origin HEAD:master
#	git add -A && \
#		git commit -m "Updated at `LANG=C date`" && \
#		git rebase origin/source && \
#		git push origin source
	lockfile-remove deploy
