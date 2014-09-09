
clean:
	@rm -fr ${BUILDDIR} dist *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name __pycache__ -name .cache -prune | xargs rm -rf
	@find . -name "*.py?" -prune | xargs rm -rf
	@find . -name "*.orig" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml


mkbuilddir:
	@mkdir -p ${BUILDDIR}


install-deps:
	@pip install --pre -qr editable_settings/requirements/develop.pip



docs: mkbuilddir intersphinx
	rm -fr docs/apidocs
	sphinx-apidoc wfp_activedirectory -H wfp-activedirectory -o docs/apidocs
	sphinx-build -n docs/ ${BUILDDIR}/docs/
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
