# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = mpim-icelab
SOURCEDIR     = source
BUILDDIR      = ../docs/_build

AUTODOCBUILD  = sphinx-apidoc
MODULEDIR     = ../src/mpim_icelab
AUTODOCDIR    = ./source/api


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help clean Makefile doc-requirements

clean:
	rm -rf $(BUILDDIR)/* $(AUTODOCDIR)

$(AUTODOCDIR): $(MODULEDIR)
	mkdir -p $@
	$(AUTODOCBUILD) --module-first -E -f -o $@ $^

doc-requirements: $(AUTODOCDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
