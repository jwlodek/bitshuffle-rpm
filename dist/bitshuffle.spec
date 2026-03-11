# Stop generation of debug rpms
%global debug_package %{nil}

Name:           bitshuffle
Version:        0.5.2
Release:        1%{?dist}
Summary:        Filter for improving compression of typed binary data.

License:        BSD-3-Clause
URL:            https://github.com/NSLS2/bitshuffle-rpm
Source0:        https://github.com/kiyo-masui/bitshuffle/archive/refs/tags/%{version}.tar.gz

BuildRequires:  hdf5-devel libzstd-devel gcc
Requires:       hdf5
Recommends:     git

BuildArch:      x86_64
#ExclusiveArch:  x86_64

# Prevent rpmbuild from smart-generating dependencies list
#AutoReq:        no

%description
Filter for improving compression of typed binary data.

%prep
%autosetup

%build

mkdir build && cd build
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../lz4/lz4.c -o lz4.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/iochain.c -o iochain.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/bitshuffle_core.c -o bitshuffle_core.o
gcc -c -fPIC -O3 -std=c99 -I../lz4 -I../src ../src/bitshuffle.c -o bitshuffle.o
gcc -shared -o libbitshuffle.so.%{version} lz4.o iochain.o bitshuffle_core.o bitshuffle.o -lhdf5 -lzstd


%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/bitshuffle

cp build/libbitshuffle.so.%{version} %{buildroot}%{_libdir}/.
ln -rs  %{buildroot}/%{_libdir}/libbitshuffle.so.%{version} %{buildroot}/%{_libdir}/libbitshuffle.so

cp src/*.h %{buildroot}%{_includedir}/bitshuffle
cp lz4/*.h %{buildroot}%{_includedir}/bitshuffle


%files
%{_libdir}/libbitshuffle*
%{_includedir}/bitshuffle/*


%changelog
* Wed Mar 11 2026 Wlodek, Jakub <jwlodek@bnl.gov> - 0.5.2-1
- Initial release of the bitshuffle library as an rpm.
