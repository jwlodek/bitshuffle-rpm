# Stop generation of debug rpms
%global debug_package %{nil}

Name:           bitshuffle
Version:        0.5.2
Release:        3%{?dist}
Summary:        Filter for improving compression of typed binary data.

License:        LicenseRef-Callaway-MIT
URL:            https://github.com/NSLS2/bitshuffle-rpm
Source0:        https://github.com/kiyo-masui/bitshuffle/archive/refs/tags/%{version}.tar.gz

BuildRequires:  hdf5-devel lz4-devel libzstd-devel gcc
Requires:       hdf5 libzstd lz4
Recommends:     git

BuildArch:      x86_64
#ExclusiveArch:  x86_64

# Prevent rpmbuild from smart-generating dependencies list
#AutoReq:        no

%description
Filter for improving compression of typed binary data.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_includedirisa} = %{version}-%{release}
Requires:       hdf5-devel
Requires:       lz4-devel
Requires:       libzstd-devel

%description devel
This package contains the header files, unversioned shared libraries
(e.g., .so files), and other resources needed for developing applications
that use %{name}.

%prep
%autosetup

%build

mkdir build && cd build
gcc -c -fPIC -O3 -std=c99 -I../src ../src/iochain.c -o iochain.o
gcc -c -fPIC -O3 -std=c99 -I../src ../src/bitshuffle_core.c -o bitshuffle_core.o
gcc -c -fPIC -O3 -std=c99 -I../src ../src/bitshuffle.c -o bitshuffle.o
# Not sure if we need to include these or not...
# gcc -c -fPIC -O3 -std=c99 -I../src ../src/bshuf_h5filter.c -o bshuf_h5filter.o
# gcc -c -fPIC -O3 -std=c99 -I../src ../src/bshuf_h5plugin.c -o bshuf_h5plugin.o

gcc -shared -Wl,-soname,libbitshuffle.so.%{version} -o libbitshuffle.so.%{version} iochain.o bitshuffle_core.o bitshuffle.o -llz4 -lhdf5 -lzstd


%install
%{__install} -d -m 0755 %{buildroot}%{_libdir}
%{__install} -d -m 0755 %{buildroot}%{_includedir}/bitshuffle

%{__install} -m 0755 build/libbitshuffle.so.%{version} %{buildroot}%{_libdir}/.
ln -s libbitshuffle.so.%{version} %{buildroot}%{_libdir}/libbitshuffle.so

cp src/*.h %{buildroot}%{_includedir}/bitshuffle

%files
%license LICENSE
%{_libdir}/libbitshuffle.so.%{version}

%files devel
%license LICENSE
%{_libdir}/libbitshuffle.so
%{_includedir}/bitshuffle/*


%changelog
* Mon Apr 20 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-3
- Use system version of lz4 library.

* Wed Mar 11 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-2
- Update permissions on main shared library file.

* Wed Mar 11 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-1
- Initial release of the bitshuffle library as an rpm.
