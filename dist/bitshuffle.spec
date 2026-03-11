# Stop generation of debug rpms
%global debug_package %{nil}

Name:           bitshuffle
Version:        0.5.2
Release:        1%{?dist}
Summary:        Filter for improving compression of typed binary data.

License:        LicenseRef-Callaway-MIT
URL:            https://github.com/NSLS2/bitshuffle-rpm
Source0:        https://github.com/kiyo-masui/bitshuffle/archive/refs/tags/%{version}.tar.gz

BuildRequires:  hdf5-devel libzstd-devel gcc
Requires:       hdf5 libzstd
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
Requires:       libzstd-devel

%description devel
This package contains the header files, unversioned shared libraries
(e.g., .so files), and other resources needed for developing applications
that use %{name}.

%prep
%autosetup

%build

mkdir build && cd build
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../lz4/lz4.c -o lz4.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/iochain.c -o iochain.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/bitshuffle_core.c -o bitshuffle_core.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/bitshuffle.c -o bitshuffle.o
gcc -shared -Wl,-soname,libbitshuffle.so.%{version} -o libbitshuffle.so.%{version} lz4.o iochain.o bitshuffle_core.o bitshuffle.o -lhdf5 -lzstd


%install
%{__install} -d -m 0755 %{buildroot}%{_libdir}
%{__install} -d -m 0755 %{buildroot}%{_includedir}/bitshuffle

%{__install} -m 0755 build/libbitshuffle.so.%{version} %{buildroot}%{_libdir}/.
ln -s libbitshuffle.so.%{version} %{buildroot}%{_libdir}/libbitshuffle.so

cp src/*.h %{buildroot}%{_includedir}/bitshuffle
cp lz4/*.h %{buildroot}%{_includedir}/bitshuffle


%files
%license LICENSE
%{_libdir}/libbitshuffle.so.%{version}

%files devel
%license LICENSE
%{_libdir}/libbitshuffle.so
%{_includedir}/bitshuffle/*


%changelog
* Wed Mar 11 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-2
- Update permissions on main shared library file.

* Wed Mar 11 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-1
- Initial release of the bitshuffle library as an rpm.
