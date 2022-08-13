# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = mpim-icelab
SOURCEDIR     = source
BUILDDIR      = _build

AUTODOCBUILD  = sphinx-apidoc
MODULEDIR     = ../src/mpim_icelab
AUTODOCDIR    = $(SOURCEDIR)/api


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help clean Makefile apidoc github

clean:
	rm -rf $(BUILDDIR)/* $(AUTODOCDIR)

github:
	@make html
	@cp -a _build/html/. ../docs

$(AUTODOCDIR): $(MODULEDIR)
	mkdir -p $@
	$(AUTODOCBUILD) --module-first -E -f -o $@ $^

apidoc: $(AUTODOCDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
