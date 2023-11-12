# We run out of memory on the ARM builders with LTO
%ifarch %{arm}
%define _lto_cflags %{nil}
%endif

# RPM macro directory
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# The source code the libint compiler generates is already very highly
# optimized.  Further optimization done by the compiler does not
# increase performance, but it just takes a *lot* longer to compile.
# We use -O2 for the compiler and -O1 for the library (these are given
# in configure). The common flags are
%global commonflags %(echo %{optflags} | sed "s|-O2||g")
%global optflags %commonflags -O1

# API version provided. Increment this whenever you change the configure time flags.
%global apiversion 0

Name:           libint2
Version:        2.7.2
Release:        1%{?dist}
Summary:        A library for efficient evaluation of electron repulsion integrals
License:        GPLv2+
URL:            https://github.com/evaleev/libint

# Compiler sources
Source0:        https://github.com/evaleev/libint/archive/v%{version}.tar.gz

# Patch lib install directory
Patch0:         libint-2.7.2-installdir.patch

Provides:       libint2(api)%{?_isa} = %{apiversion}

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  boost-devel
BuildRequires:  mpfr-devel
BuildRequires:  python3-devel
BuildRequires:  cmake
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  doxygen
BuildRequires:  eigen3-devel
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  texlive-algorithms
BuildRequires:  texlive-appendix
BuildRequires:  texlive-bbding
BuildRequires:  texlive-firstaid
BuildRequires:  texlive-framed
BuildRequires:  texlive-graphics
BuildRequires:  texlive-mathcomp
BuildRequires:  texlive-sfmath
BuildRequires:  texlive-subfigure
BuildRequires:  texlive-wrapfig

%description
LIBINT computes the Coulomb and exchange integrals, which in electronic
structure theory are called electron repulsion integrals (ERIs). This is by
far the most common type of integrals in molecular structure theory.

LIBINT uses recursive schemes that originate in seminal Obara-Saika method and
Head-Gordon and Pople’s variation thereof. The idea of LIBINT is to optimize
computer implementation of such methods by implementing an optimizing compiler
to generate automatically highly-specialized code that runs well on
super-scalar architectures.

%package doc
Summary:        Documentation for libint
Requires:       libint2 = %{version}-%{release}

%description doc
This package contains a programmer's manual and doxygen documentation
for the classes.

%package devel
Summary:        Development headers and libraries for libint
Requires:       libint2%{?_isa} = %{version}-%{release}
# For dir ownership
Requires:       cmake

%description devel
This package contains development headers and libraries for libint.

%prep
%setup -q -n libint-%{version}
%patch0 -p1
sed -i "s#\today#June 20, 2022#" doc/progman/progman.tex
./autogen.sh
cd ..
mv libint-%{version} libint-%{version}-bootstrap
cp -ar libint-%{version}-bootstrap libint-%{version}
cd libint-%{version}
./configure --enable-shared --disable-static --enable-fortran
%__make pdf html -j
mkdir -p ../libint-%{version}-tmp/doc
cp -a doc/progman/progman.pdf ../libint-%{version}-tmp/doc/
cp -ar doc/classdoc/html ../libint-%{version}-tmp/
cd ..
rm -rf libint-%{version}
cp -ar libint-%{version}-bootstrap libint-%{version}
cd libint-%{version}
./configure --enable-shared --disable-static \
 --enable-eri=2 --enable-eri3=2 --enable-eri2=2 --with-eri-max-am=7,5,4 \
 --with-eri-opt-am=3 --with-eri3-max-am=7 --with-eri2-max-am=7 \
 --with-g12-max-am=5 --with-g12-opt-am=3 --with-g12dkh-max-am=5 \
 --with-g12dkh-opt-am=3 --with-multipole-max-order=10 --enable-1body=2 \
 --disable-unrolling --enable-generic-code \
 --enable-contracted-ints --with-incdirs="-I%{_includedir}/eigen3"\
 --with-cxx-optflags="-O2" CXX=g++
##  --with-cxx-optflags="-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection"
%__make export -j
mv libint-%{version}.tgz ../
cd ..
rm -rf libint-%{version}
tar -xf libint-%{version}.tgz
cp -far libint-%{version}-tmp/* libint-%{version}/
cd libint-%{version}

%build
%cmake -DENABLE_FORTRAN=ON -DLIBINT2_BUILD_SHARED_AND_STATIC_LIBS=ON
%cmake_build

%install
%cmake_install
# Get rid of the basis set files that ship with libint
find %{buildroot}%{_datadir}/libint -name \*.g94 -delete

# Create macro file
mkdir -p %{buildroot}%{macrosdir}
cat > %{buildroot}%{macrosdir}/macros.libint2 << EOF
# Current version of libint2 is
%_libint2_apiversion %{apiversion}
EOF

# Move module file to the correct location
mkdir -p %{buildroot}%{_fmoddir}
mv %{buildroot}%{_includedir}/libint_f.mod %{buildroot}%{_fmoddir}/

%ldconfig_scriptlets

%files
%doc LICENSE COPYING
%{_libdir}/libint*.so*

%files doc
%doc doc/progman.pdf html

%files devel
%{macrosdir}/macros.libint2
%{_libdir}/cmake/libint2/
%{_includedir}/libint2/
%{_includedir}/libint2.h
%{_includedir}/libint2.hpp
%{_libdir}/libint*.a
%{_libdir}/pkgconfig/libint2.pc
%{_fmoddir}/libint_f.mod

%changelog
* Sat Nov 11 2023 L <lunusvir@gmail.com> - 2.7.2-1
- Update to 2.7.2.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 21 2021 Jeff Law <law@redhat.com> - 2.6.0-10
- Disable LTO on arm

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 20 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.0-8
- Add BR: python3-devel.

* Tue Sep 29 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.0-7
- Disable buggy Eigen3 support until 2.7.0 is released.

* Sun Aug 16 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.0-6
- Enable Eigen3 support in build.

* Fri Aug 14 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.0-5
- Enable Fortran bindings.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 02 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 2.1.0-2
- Rebuilt for Boost 1.63

* Sun Jul 10 2016 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0.

* Fri Jul 08 2016 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-17.644hg
- Use pregenerated programmer's manual when not bootstrapping.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-16.644hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 2.0.3-15.644hg
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2.0.3-14.644hg
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-13.644hg
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 2.0.3-12.644hg
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-11.644hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.3-10.644hg
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 2.0.3-9.644hg
- Rebuild for boost 1.57.0

* Tue Sep 09 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-8.644hg
- Provide libint2(api) and rpm macro.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-7.644hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6.644hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 2.0.3-5.644hg
- Rebuild for boost 1.55.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4.644hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 2.0.3-3.644hg
- Rebuild for boost 1.54.0

* Thu Jul 11 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-1.644hg
- Use xz to compress tarballs (BZ #979817).
- Update to revision 644.

* Tue May 21 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-2.641hg
- Reduce maximum angular momentum for derivative ERIs, since 2nd derivatives of
  (kk|kk) takes more than 2 GB of RAM.
- Enabled g12 and g12dkh integrals.

* Thu May 16 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.3-1.641hg
- Use pregenerated tarballs only on EPEL.

* Sun May 12 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.2-2.618hg
- Switch to using a pregenerated tarball of library sources instead of
  rerunning compiler for each build, solving BZ #961963.

* Thu May 09 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.2-1.615hg
- Update to hg snapshot 615 (version 2.0.2), fixing FTBFS on rawhide.
- Added possibility to run tests, but not by default since running them
  takes *eons*.

* Mon May 06 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.0-3.607hg
- Explicitly arched requires in -devel package.

* Mon Feb 18 2013 Dominik Mierzejewski <rpm@greysector.net> - 2.0.0-2.607hg
- Add missing tex build dependencies
- Fix devel subpackage dependencies

* Wed Jan 23 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.0.0-1.607hg
- First release.