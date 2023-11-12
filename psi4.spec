%define _smp_build_ncpus 12
%define _gcc_lto_cflags -flto=8 -fno-fat-lto-objects -fuse-linker-plugin
%define _general_options -O2 %{?_lto_cflags} -fexceptions -g -g1 -grecord-gcc-switches -pipe
%define __ld /usr/bin/ld.gold
%define build_ldflags -fuse-ld=gold -Wl,-z,relro %{_ld_as_needed_flags} %{_ld_symbols_flags} %{_hardened_ldflags} %{_annotation_ldflags} %[ "%{toolchain}" == "clang" ? "%{?_clang_extra_ldflags}" : "" ] %{_build_id_flags} %{?_package_note_flags} -L%{_prefix}/lib64

%global debug_package %{nil}
%global psi4_build_type Release

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global cmake_blas_flags -DBLAS_TYPE=FLEXIBLAS -DLAPACK_TYPE=FLEXIBLAS
%else
%global blaslib openblas
%global blasvar o
%global cmake_blas_flags -DBLAS_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so -DLAPACK_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so
%endif

%global commonflags %(echo %{optflags} | sed "s/-O[0123s]//g" | sed "s/-Wp,-D_GLIBCXX_ASSERTIONS//g")
%global optflags %commonflags -O2 -fno-strict-aliasing

%global git_hash df9a0dd5b3fa8dda9d400fd928b149af42ca39af
%global git_short_hash df9a0dd

%global libint2_pregenerated ON
%global libint2_MAX_ERI_AM 7
%global _external_force_build ON
%global _external_build_static ON

Name:           psi4
Epoch:          1
Version:        1.8.3dev60
Release:        1%{?dist}
Summary:        An ab initio quantum chemistry package
License:        LGPLv3 and MIT
URL:            http://www.psicode.org/
Source0:        psi4-%{git_short_hash}.tar.gz

Source1:        adcc-0.15.16.tar.gz
Source2:        cct3-bff480f.tar.gz
Source3:        gpu_dfcc-b98c6f1.tar.gz
Source4:        psi4pasture-f10345d.tar.gz
Source5:        psi4fockci-267e171.tar.gz
Source6:        sns-mp2-12462c6.tar.gz
Source7:        v2rdm_casscf-aa7d6a1.tar.gz
Source8:        ambit-733c529.tar.gz
Source9:        CheMPS2-d8ac508.tar.gz
Source10:       cppe-0.3.1.tar.gz
Source11:       ddX-0.4.5.tar.gz
Source12:       dkh-3ba0128.tar.gz
Source13:       libecpint-1.0.7.tar.gz
Source14:       erd-3.0.6.tar.gz
Source15:       gau2grid-2.0.7.tar.gz
Source16:       gdma-2.3.3.tar.gz
Source17:       GTFock-8dc3519.tar.gz
Source18:       libefp-15cd7ce.tar.gz
Source19:       libint-935d379.tar.gz
Source20:       libint-2.7.2-post1-5-4-3-6-5-4_mm4f12ob2_1.tgz
%global libint2_tarball_name libint-0eca57e.tar.gz
%global libint2_directory_name libint-0eca57e412cd93c72c01fa0173698f9a082b475b
Source21:       %{libint2_tarball_name}
Source22:       libint-577d295.tar.gz
Source23:       libxc-6.2.2.tar.gz
Source24:       MDI_Library-1.2.3.tar.gz
Source25:       optking-0.2.1.tar.gz
Source26:       pcmsolver-v123_plus_ming.tar.gz
Source27:       pybind11-2.10.3.tar.gz
Source28:       pylibefp-0.6.1.tar.gz
Source29:       QCElemental-0.26.0.tar.gz
%global qcengine_tarball_name QCEngine-0.28.1.tar.gz
%global qcengine_directory_name QCEngine-0.28.1
Source30:       %{qcengine_tarball_name}
Source31:       simint-v0.7.tar.bz2
Source32:       basis_set_exchange-0.9.tar.gz
Source60:       libint-2.7.2-post1-7-7-4-7-7-5_mm4f12ob2_1.tgz

# Use system packages
Patch0:         psi4-1.8-fedora.patch
# Use python3 not python in test runner
Patch1:         psi4-1.8-python3.patch
# Remove rpath
Patch2:         psi4-1.8-rpath.patch

# SRPM containing external dependencies
Patch3:         psi4-1.8-selfcontained.patch
Patch4:         libint-577d295-fedora.patch
Patch5:         psi4-1.8-force_build.patch
Patch6:         psi4-1.8-force_build_python.patch
Patch7:         psi4-1.8-build_shared.patch
Patch8:         psi4-1.8-build_static.patch
Patch9:         psi4-stage-ambit_pcm.patch

BuildRequires:  cmake
BuildRequires:  bison-devel
BuildRequires:  byacc
BuildRequires:  binutils-gold
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  boost-devel
BuildRequires:  perl-devel
BuildRequires:  gsl-devel
BuildRequires:  hdf5-devel
BuildRequires:  zlib-devel
BuildRequires:  gmp-devel

BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++-static
BuildRequires:  libgfortran-static
BuildRequires:  %{blaslib}-devel
#BuildRequires:  CheMPS2-devel
#BuildRequires:  libint-devel >= 1.1.5-3
BuildRequires:  eigen3-devel
#BuildRequires:  libxc-devel
#BuildRequires:  pybind11-static
#BuildRequires:  gau2grid-devel
#BuildRequires:  libefp-devel

BuildRequires:  python3-devel >= 2.7
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python3-sphinx >= 1.1
BuildRequires:  python3-pydantic
BuildRequires:  python3-qcelemental
BuildRequires:  python3-qcengine
BuildRequires:  python3-optking
BuildRequires:  python3-cpuinfo
# These are required also at runtime
#Requires:       gau2grid
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-pydantic
Requires:       python3-qcelemental
Requires:       python3-qcengine
Requires:       python3-optking
Requires:       python3-deepdiff
Requires:       python3-cpuinfo
Requires:       python3-psutil
Requires:       python3-pint
Requires:       python3-networkx

# For the documentation
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  dvipng
BuildRequires:  graphviz

%if %{with tests}
# Needed for running tests
BuildRequires:  perl(Env)
%endif

Requires:  %{name}-data = %{epoch}:%{version}-%{release}
# Libint can break the api between releases
#Requires:  libint(api)%%{?_isa} = %%{_libint_apiversion}

# Don't have documentation in the cmake version yet.. 
Obsoletes: psi4-doc < 1:0.3-1

%description
PSI4 is an open-source suite of ab initio quantum chemistry programs
designed for efficient, high-accuracy simulations of a variety of
molecular properties. We can routinely perform computations with more
than 2500 basis functions running serially or in parallel.


%package data
Summary:   Data files necessary for operation of PSI4
BuildArch: noarch

%description data
This package contains necessary data files for PSI4, e.g., basis sets
and the quadrature grids.


%package devel
Summary:   Static libraries and development headers for psi
Requires:  %{name}%{?_isa} = %{epoch}:%{version}-%{release}
# For dir ownership
Requires:  cmake

%description devel
This package contains static libraries and development headers for psi.

%prep
%setup -q -n psi4-%{git_hash}
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%if "%{_external_force_build}" == "ON"
%patch 5 -p1
%endif
%if "%{_external_build_static}" == "ON"
%patch 8 -p1
%else
%patch 7 -p1
%endif

cp "%{SOURCE1}" "external/downstream/adcc/"
cp "%{SOURCE2}" "external/downstream/cct3/"
cp "%{SOURCE3}" "external/downstream/gpu_dfcc/"
cp "%{SOURCE4}" "external/downstream/pasture/"
cp "%{SOURCE5}" "external/downstream/psi4fockci/"
cp "%{SOURCE6}" "external/downstream/snsmp2/"
cp "%{SOURCE7}" "external/downstream/v2rdm_casscf/"
cp "%{SOURCE8}" "external/upstream/ambit/"
cp "%{SOURCE9}" "external/upstream/chemps2/"
cp "%{SOURCE10}" "external/upstream/cppe/"
cp "%{SOURCE11}" "external/upstream/ddx/"
cp "%{SOURCE12}" "external/upstream/dkh/"
cp "%{SOURCE13}" "external/upstream/ecpint/"
cp "%{SOURCE14}" "external/upstream/erd/"
cp "%{SOURCE15}" "external/upstream/gau2grid/"
cp "%{SOURCE16}" "external/upstream/gdma/"
cp "%{SOURCE17}" "external/upstream/gtfock/"
cp "%{SOURCE18}" "external/upstream/libefp/"
cp "%{SOURCE19}" "external/upstream/libint/"
%if "%{libint2_pregenerated}" == "ON"
cp "%{SOURCE20}" "external/upstream/libint2/"
cp "%{SOURCE60}" "external/upstream/libint2/"
%else
cp "%{SOURCE21}" "external/upstream/libint2/"
pushd "external/upstream/libint2/"
tar -xf "%{libint2_tarball_name}"
rm -f "%{libint2_tarball_name}"
pushd "%{libint2_directory_name}"
patch -d . --reject-format=unified -p1 -i "%{PATCH4}"
popd
tar -czf "%{libint2_tarball_name}" "%{libint2_directory_name}"
rm -rf "%{libint2_directory_name}"
popd
%endif
cp "%{SOURCE23}" "external/upstream/libxc/"
cp "%{SOURCE24}" "external/upstream/mdi/"
cp "%{SOURCE25}" "external/upstream/optking/"
cp "%{SOURCE26}" "external/upstream/pcmsolver/"
cp "%{SOURCE27}" "external/upstream/pybind11/"
cp "%{SOURCE28}" "external/upstream/pylibefp/"
cp "%{SOURCE29}" "external/upstream/qcelemental/"
cp "%{SOURCE30}" "external/upstream/qcengine/"
pushd "external/upstream/qcengine/"
tar -xf "%{qcengine_tarball_name}"
rm -f "%{qcengine_tarball_name}"
sed -i 's#"python"#"python3"#' "%{qcengine_directory_name}/qcengine/programs/psi4.py"
tar -czf "%{qcengine_tarball_name}" "%{qcengine_directory_name}"
rm -rf "%{qcengine_directory_name}"
popd
cp "%{SOURCE31}" "external/upstream/simint/"
cp "%{SOURCE32}" "external/upstream/bse/"

%build
export F77=gfortran
export FC=gfortran

# Massage the Python site directory for the installer
export pymoddir=$(echo %{python3_sitearch} | sed "s|%{_libdir}||g")

%cmake \
       -DMAX_AM_ERI=%{libint2_MAX_ERI_AM} \
       -DENABLE_OPENMP=ON -DENABLE_GENERIC=OFF -DENABLE_MPI=OFF -DENABLE_XHOST=OFF \
       -DPYMOD_INSTALL_LIBDIR=${pymoddir} \
       %{cmake_blas_flags} -DENABLE_AUTO_LAPACK=ON \
       -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ \
       -DCUSTOM_C_FLAGS='%{optflags} -std=c11 -DNDEBUG' -DCUSTOM_CXX_FLAGS='%{optflags} -DNDEBUG' \
       -DCUSTOM_Fortran_FLAGS='-I%{_libdir}/gfortran/modules %{optflags} -DNDEBUG' \
       -DCMAKE_BUILD_TYPE=%{psi4_build_type} -DCMAKE_INSTALL_LIBDIR="%{_lib}" \
       -DENABLE_ambit=ON \
       -DENABLE_CheMPS2=ON \
       -DENABLE_dkh=ON \
       -DENABLE_gdma=ON \
       -DENABLE_ecpint=ON \
       -DENABLE_PCMSolver=ON \
       -DENABLE_simint=ON \
       -DENABLE_libefp=OFF \
       -DENABLE_pylibefp=OFF \
       -DSIMINT_VECTOR=scalar \
%if "%{libint2_pregenerated}" == "ON"
       -DBUILD_Libint2_GENERATOR=OFF
%else
       -DBUILD_Libint2_GENERATOR=ON -DCMAKE_DISABLE_FIND_PACKAGE_Libint2=ON
%endif

# Build program
%cmake_build

%global stage_python3_sitearch %(echo %{python3_sitearch} | sed "s#^/usr##")
%global stage_fullpath %{_builddir}/psi4-%{git_hash}/redhat-linux-build/stage
pushd redhat-linux-build
patch -d . --reject-format=unified -p1 -i "%{PATCH9}"
mkdir -p stage/%{stage_python3_sitearch}/psi4/external
mv stage/%{stage_python3_sitearch}/pcmsolver stage/%{stage_python3_sitearch}/psi4/external/
mv stage/%{stage_python3_sitearch}/gdma* stage/%{stage_python3_sitearch}/psi4/external/
sed -i -e 's#%{stage_fullpath}#/usr#' stage/%{stage_python3_sitearch}/psi4/__init__.py
find stage/%{stage_python3_sitearch}/psi4 -name '*.py' | while IFS= read -r f; do
sed -i -e 's|which_import("gdma"|which_import("psi4.external.gdma"|' $f
sed -i -e 's|^\([^#]*\)import gdma|\1from psi4.external import gdma|' $f
done
popd

%install
%cmake_install

mv %{buildroot}%{_bindir}/gdma %{buildroot}%{_bindir}/psi4_gdma
mv %{buildroot}%{_bindir}/go_pcm.py %{buildroot}%{_bindir}/psi4_go_pcm.py
mv %{buildroot}%{_bindir}/plot_cavity.py %{buildroot}%{_bindir}/psi4_plot_cavity.py

# Get rid of spurious files
rm -rf %{buildroot}%{_builddir}
rm -rf %{buildroot}%{_datadir}/TargetHDF5/
rm -rf %{buildroot}%{_datadir}/TargetLAPACK/
rm -rf %{buildroot}%{_datadir}/TargetHDF5/
rm -rf %{buildroot}%{_datadir}/cmake/TargetHDF5/
rm -rf %{buildroot}%{_datadir}/cmake/TargetLAPACK/

rm -rf %{buildroot}%{_includedir}/libint2*
rm -rf %{buildroot}%{_libdir}/cmake/libint2*
rm -rf %{buildroot}%{_libdir}/pkgconfig/libint2*
rm -f %{buildroot}%{_libdir}/libint2*
rm -rf %{buildroot}%{_datadir}/libint*
find %{_exec_prefix}/lib/debug -name 'libint*.debug' -delete

rm -f %{buildroot}%{_bindir}/xc-info
rm -f %{buildroot}%{_includedir}/libxc.bib
rm -rf %{buildroot}%{_includedir}/xc*
rm -f %{buildroot}%{_libdir}/libxc*
rm -f %{buildroot}%{_libdir}/pkgconfig/libxc*
rm -rf %{buildroot}%{_libdir}/pylibxc
rm -rf %{buildroot}%{_libdir}/Libxc
rm -rf %{buildroot}%{_libdir}/cmake/Libxc

rm -rf %{buildroot}%{_includedir}/gau2grid*
rm -f %{buildroot}%{_libdir}/libgg*
rm -rf %{buildroot}%{_datadir}/gau2grid*
rm -rf %{buildroot}%{_datadir}/cmake/gau2grid*

rm -f %{buildroot}%{_bindir}/chemps2*
rm -rf %{buildroot}%{_includedir}/chemps2*
rm -f %{buildroot}%{_libdir}/libchemps2*
rm -rf %{buildroot}%{_datadir}/CheMPS2*
rm -rf %{buildroot}%{_datadir}/cmake/CheMPS2*
find %{_exec_prefix}/lib/debug -name 'chemps2*.debug' -delete

rm -rf %{buildroot}%{_includedir}/ambit
rm -f %{buildroot}%{_libdir}/libambit*
rm -rf %{buildroot}%{_datadir}/cmake/ambit
rm -rf %{buildroot}%{python3_sitearch}/ambit

rm -rf %{buildroot}%{_includedir}/DKH
rm -f %{buildroot}%{_libdir}/libdkh*
rm -rf %{buildroot}%{_datadir}/cmake/dkh

rm -rf %{buildroot}%{_includedir}/GDMA
rm -f %{buildroot}%{_libdir}/libgdma*
rm -rf %{buildroot}%{_datadir}/cmake/gdma

rm -rf %{buildroot}%{_includedir}/libecpint*
rm -f %{buildroot}%{_libdir}/libecpint*
rm -f %{buildroot}%{_libdir}/libFaddeeva*
rm -rf %{buildroot}%{_libdir}/cmake/ecpint*
rm -rf %{buildroot}%{_datadir}/libecpint

rm -rf %{buildroot}%{_includedir}/PCMSolver
rm -f %{buildroot}%{_libdir}/libpcm*
rm -rf %{buildroot}%{_datadir}/cmake/PCMSolver

rm -rf %{buildroot}%{_includedir}/pybind11
rm -rf %{buildroot}%{_datadir}/cmake/pybind11
rm -rf %{buildroot}%{_datadir}/pkgconfig/pybind11.pc

rm -rf %{buildroot}%{_includedir}/simint
rm -f %{buildroot}%{_libdir}/libsimint*
rm -rf %{buildroot}%{_datadir}/cmake/simint


%check
# Run quick tests to see the program works.
# quicktests are too long, whole test suite way too long.
cd %{_vpath_builddir}/tests
ctest -L smoketests

%files
%license COPYING COPYING.LESSER
%doc README.md
%{python3_sitearch}/psi4/
%{_bindir}/psi4
%{_bindir}/psi4_gdma
%{_bindir}/psi4_go_pcm.py
%{_bindir}/psi4_plot_cavity.py

%files data
%license COPYING COPYING.LESSER
%{_datadir}/psi4/

%files devel
%license COPYING COPYING.LESSER
%{_datadir}/cmake/psi4/
%{_includedir}/psi4/

%changelog
* Sat Nov 11 2023 L <lunusvir@gmail.com> - 1:1.8.2dev60-1
- Update psi4 to commit df9a0dd.
- Update external libraries.
- Build static external libraries.
- Patch libint2 configuration.
- Use pre-generated sources for libint2. AM = 7.
- Disable _GLIBCXX_ASSERTIONS to work around uses of vector::operator[].

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 1:1.3.2-12
- Add a patch for native support of FlexiBLAS
- Explicitly turn ENABLE_AUTO_LAPACK on

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:1.3.2-11
- Rebuilt for Python 3.10

* Wed Mar 31 2021 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.3.2-10
- Make the psi4 Python module importable.
- Remove rpath.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Jeff Law <law@redhat.com> - 1:1.3.2-8
- Do not force C++11 mode

* Sun Aug 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1:1.3.2-7
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Wed Aug 05 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.3.2-6
- Adapt to new CMake scripts.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.3.2-3
- Rebuild against libxc 5 in rawhide.
- Add missing deepdiff requires.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.3.2-1
- Update to 1.3.2.

* Mon Mar 04 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.3.0-1
- Update to 1.3.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.1-5.b167f47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.2.1-4.b167f473git
- Add deepdiff requires.

* Sun Dec 09 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.2.1-3.b167f47
- Require python3-numpy instead of python2-numpy

* Wed Sep 26 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.2.1-2.b167f473git
- Update to git snapshot to make code run with -D_GLIBCXX_ASSERTIONS.

* Sat Sep 22 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.2.1-1
- Update to 1.2.1.

* Fri Aug 10 2018 Marcel Plch <mplch@redhat.com> - 1:1.1-8.add49b9git
- Patch for pybind 2.2.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-7.add49b9git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.1-6.add49b9git
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-5.add49b9git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-4.add49b9git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-3.add49b9git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 19 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.1-2.add49b95git
- Epoch was missing from a requires.

* Wed May 17 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.1-1.add49b95git
- Update to version 1.1. License changes from GPLv2+ to LGPLv3.
- Make sure binary is linked to right atlas library.

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-3.2118f2fgit
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Thu Mar 02 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.0-2.2118f2f5git
- Update to get patch that fixes build on rawhide.

* Mon Feb 27 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.0-1.926879e2git
- Update to newest git snapshot.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0-0.3.rc.15fc63cgit
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1:1.0-0.2.rc.15fc63cgit
- Rebuilt for Boost 1.63

* Thu Jun 02 2016 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:1.0-0.1.rc.15fc64cgit
- Update to 1.0 release candidate.

* Tue May 17 2016 Jonathan Wakely <jwakely@redhat.com> - 1:0.3-7.1881450git
- Rebuilt for linker errors in boost (#1331983)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3-6.1881450git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 1:0.3-5.1881450git
- Rebuilt for Boost 1.60

* Wed Sep 09 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3-4.1881450fgit
- Use narrowing patch from upstream instead of -Wno-narrowing.

* Tue Sep 08 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3-3.1881450fgit
- Add epoch to explicit requires.

* Tue Sep 08 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3-2.1881450fgit
- Patch to fix broken linkage.

* Sun Sep 06 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3-1.1881450fgit
- Update to newest release, switched to using github release tags.

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.21.c7deee9git.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 4.0-0.20.c7deee9git.1
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.19.c7deee9git.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.0-0.18.c7deee9git.1
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 4.0-0.17.c7deee9git.1
- Rebuild for boost 1.57.0

* Thu Sep 11 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.16.c7deee99.1
- Forgot to tag buildroot override in previous build.

* Wed Sep 10 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.16.c7deee99
- Update to newest snapshot.
- Requires libint(api).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.15.0c7ea92git.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.14.0c7ea92git.1
- Rebuild due to rebuilt libint.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.14.0c7ea92git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 4.0-0.13.0c7ea92git
- Rebuild for boost 1.55.0

* Tue May 13 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.12.0c7ea928git
- Add BR: perl(Env) for tests.

* Tue May 13 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.11.0c7ea928git
- Update to newest git snapshot.
- Remove BR: ruby-devel.

* Mon Mar 10 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.10.b5
- Rebuild against updated libint.

* Sat Jan 04 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.9.b5
- Drop %%?_isa from virtual provide of -static package (BZ #951582).

* Fri Dec 27 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.8.b5
- Versioned libint build dependency.

* Tue Dec 24 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.7.b5
- Added LICENSE and COPYING to -data as well.
- Versioned libint dependency.

* Sat Dec 21 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.6.b5
- Get rid of bundled madness.

* Thu Dec 19 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.5.b5
- Added BR and R on numpy.
- Use ATLAS after all.

* Fri Aug 16 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.4.b5
- Use openblas on supported architectures.
- Update to beta5.

* Thu May 02 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.3.b4
- Added BR on graphviz and enabled dot in configure for documentation.

* Tue Apr 30 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.2.b4
- Review fixes.

* Thu Apr 11 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0-0.1.b4
- First release.
