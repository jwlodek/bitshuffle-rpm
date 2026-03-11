all: rpm srpm

clean:
	rm -rf BUILD RPMS SRPMS SPECS SOURCES BUILDROOT
	rm -f *.rpm *.srpm

rpm:
	mkdir -p SOURCES
	rpmbuild -v --noclean \
            --define "_topdir $(PWD)" \
            --define "buildroot %{_topdir}/BUILDROOT" \
            --undefine=_disable_source_fetch \
            --define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
            -bb ./dist/*.spec
	cp RPMS/*.rpm .

srpm:
	mkdir -p SOURCES
	rpmbuild -v --noclean \
            --define "_topdir $(PWD)" \
            --define "buildroot %{_topdir}/BUILDROOT" \
            --undefine=_disable_source_fetch \
            --define "_srpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.src.rpm" \
            -bs ./dist/*.spec
	cp SRPMS/*.src.rpm .
