# Warning:
# Anyone editing this spec file please make sure the same spec file
# works on other fedora and epel releases, which are supported by this software.
# No quick Rawhide-only fixes will be allowed.

%if 0%{?el6}
gfortran < 4.9 unsupported https://gitlab.com/QEF/q-e/issues/113
%quit
%endif

%if 0%{?el7}
# Error: Assumed-shape array 'zvec' at (1) cannot be an argument to the procedure 'c_loc' because it is not C interoperable
gfortran < 4.9 unsupported https://lists.quantum-espresso.org/pipermail/users/2020-November/046420.html
%quit
%endif

%global PIFLAG -fPIE
%global WPICFLAG --without-pic

%if 0%{?fedora} >= 32 || 0%{?rhel} >= 9
# -fallow-argument-mismatch is a workaround to compile UtilXlib/mp.f90
# "Type mismatch between actual argument at (1) and actual argument at (2)"
# Use -fno-lto on f36 gfortran-12 https://gitlab.com/QEF/q-e/-/issues/460
%global extra_gfortran_flags -fallow-argument-mismatch -fno-lto %{PIFLAG}
%else
%global extra_gfortran_flags %{PIFLAG}
#%%{nil}
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
%global python python3
%else
%global python python
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%else
%global blaslib openblas
%endif

# devxlib compilation fails on armv7hl
# configure: error: cannot guess build type; you must specify one
ExclusiveArch:		x86_64 %{ix86} aarch64 %{power64}

# disable compilation warnings
%global wnoflags -Wno-unused-variable -Wno-conversion -Wno-unused-dummy-argument -Wno-character-truncation -Wno-missing-include-dirs -Wno-unused-function -Wno-maybe-unitialized

%global qe_version              7.3dev405
%global qe_commit               4081977477a4471b3e1805f7f015122ebbe1cfbb
%global d3q_commit              2c41405306b1aaecb8dcce2fe9f50631828152ec
%global devxlib_commit          0.2.0
%global fox_commit              4.1.2-QE
%global mbd_commit              cbc82c459b6ca4de161bac7e3e1005f4f40430ae
%global pw2qmcpack_commit       3e0ad027fbd30eb52176abd8affcb66d4ce6f5b3
%global gipaw_commit            7.2
%global wannier90_commit        d141f9f84dcd3ac54729b9e5874dabd451684237
%global want_commit             2.6.1
%global yambo_commit            497f6fbd95db5792b04fb141ea944e5751a4a504
%global w90_path                external/wannier90

Name:			quantum-espresso
Version:		%{qe_version}
Release:		1%{?dist}
Summary:		A suite for electronic-structure calculations and materials modeling

# See bundling discussion in https://gitlab.com/QEF/q-e/-/issues/366
Provides:               bundled(FoXlibf)
Provides:               bundled(deviceXlib)
Provides:               bundled(libmbd)
Provides:               bundled(wannier90)
Provides:               bundled(qe-gipaw)
Provides:               bundled(d3q)
Provides:               bundled(yambo)

License:		GPLv2+
# BSD: PP/src/bgw2pw.f90
# BSD: PP/src/pw2bgw.f90
# LGPLv2+: Modules/bspline.f90
# MIT: install/install-sh
# zlib/libpng: clib/md5.c
# zlib/libpng: clib/md5.h
URL:			http://www.quantum-espresso.org/
Source0:		https://github.com/QEF/q-e/archive/refs/tags/qe-%{qe_commit}.tar.gz

# pseudopotentials not included in the source and needed by PW/tests
# cd test-suite && make pseudo
Source1:		pseudo.tar.gz

# Bundle gitlab.com/max-centre/components/devicexlib
Source2:		devicexlib-%{devxlib_commit}.tar.gz
Source3:		d3q-%{d3q_commit}.tar.gz
Source4:		fox-%{fox_commit}.tar.gz
Source5:		libmbd-%{mbd_commit}.tar.gz
Source6:		pw2qmcpack-%{pw2qmcpack_commit}.tar.gz
Source7:		qe-gipaw-%{gipaw_commit}.tar.gz
Source8:		wannier90-%{wannier90_commit}.tar.gz
Source9:		want-%{want_commit}.tar.gz
Source10:		yambo-%{yambo_commit}.tar.gz
Source11:		yambo-libraries-%{yambo_commit}.tar

Patch0:			qe-ext.patch
Patch1:			qe-gipaw-revert_c8e2a3f.patch
Patch2:			qe-ext-d3q.patch
Patch3:			qe-ext-yambo.patch

# handle license on el{6,7}: global must be defined after the License field above
%{!?_licensedir: %global license %doc}

BuildRequires:		git
BuildRequires:		autoconf
BuildRequires:		autogen
BuildRequires:		automake
BuildRequires:		libtool
BuildRequires:		hostname
BuildRequires:		m4
BuildRequires:		make
BuildRequires:		cmake
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:		python3
BuildRequires:		python3-numpy
%else
BuildRequires:		python
BuildRequires:		numpy
%endif
BuildRequires:		gcc-g++
BuildRequires:		gcc-gfortran
BuildRequires:		%{blaslib}-devel
BuildRequires:		blas-devel
# Use openblas-serial instead of openblas-openmp
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
BuildRequires:		flexiblas-openblas-serial
Requires:		flexiblas-openblas-serial
%endif
BuildRequires:		fftw3-devel

BuildRequires:		openssh-clients
BuildRequires:		which

Requires:		openssh-clients

#BuildRequires:		hdf5-devel
#Requires:		hdf5

BuildRequires:		libzip-devel
Requires:		libzip
BuildRequires:		zlib-devel
Requires:		zlib

BuildRequires:		libxc-devel
Requires:		libxc

%global desc_base \
QUANTUM ESPRESSO is an integrated suite of Open-Source computer codes for\
electronic-structure calculations and materials modeling at the nanoscale.\
It is based on density-functional theory, plane waves, and pseudopotentials.


%description
%{desc_base}

Serial version.


%package openmpi
Summary:		%{name} - openmpi version
BuildRequires:		openmpi-devel
BuildRequires:		scalapack-openmpi-devel
#BuildRequires:		hdf5-openmpi-devel
Requires:		openmpi
#Requires:		hdf5-openmpi
%if 0%{?el7}
Requires:		scalapack-openmpi
Requires:		blacs-openmpi
%endif

%description openmpi
%{desc_base}

This package contains the openmpi version.


%package mpich
Summary:		%{name} - mpich version
BuildRequires:		mpich-devel
BuildRequires:		scalapack-mpich-devel
#BuildRequires:		hdf5-mpich-devel
Requires:		mpich
#Requires:		hdf5-mpich
%if 0%{?el7}
Requires:		scalapack-mpich
Requires:		blacs-mpich
%endif

%description mpich
%{desc_base}

This package contains the mpich version.


%prep
%setup -q -n q-e-qe-%{qe_commit}
%patch -P0 -p1

sed -i -e 's#rm -f \.\./bin/wannier90\.x#rm -f ../bin/wannier90.x ../bin/postw90.x ../bin/w90chk2chk.x ../bin/w90spn2spn.x ../bin/w90pov.x ../bin/w90vdw.x#' install/plugins_makefile
echo 'define download_and_unpack'  >  install/install_utils
echo '  @(echo "download $(2).")'  >> install/install_utils
echo 'endef'                       >> install/install_utils
echo 'define update_submodule'     >> install/install_utils
echo '  @(echo "submodule $(2).")' >> install/install_utils
echo 'endef'                       >> install/install_utils

%global clean_externals() \
for e in hdf5 devxlib d3q fox mbd pw2qmcpack qe-gipaw wannier90 want yambo; do \
if [[ -e external/$e ]]; then rm -rf external/$e; fi \
mkdir -p external/$e \
done && \
for l in hdf5 D3Q GIPAW W90 WANT YAMBO; do \
if [[ -L $l ]]; then rm -f $l \
elif [[ -d $l ]]; then rm -rf $l; fi \
done

%global prepare_yambo_externals() \
if [[ ! -e external/yambo_externals ]]; then \
mkdir -p external/yambo_externals && \
tar -xf %{SOURCE11} -C external/yambo_externals/ &&\
pushd external/yambo_externals &&\
for tarball in Ydriver*.tar.gz; do \
mkdir tmp &&\
tar -xf "$tarball" -C tmp/ &&\
rm -f "$tarball" &&\
cd tmp &&\
for f in $(find -name '*.m4' -or -name 'configure'); do \
sed -i -e 's#\\(FC\\?UFLAGS="[^$]*\\)"#\\1 %{PIFLAG}"#' "$f" \
done &&\
tar -czf ../"$tarball" * && cd .. &&\
rm -rf tmp \
done &&\
popd \
fi

%global prepare_externals() \
%clean_externals &&\
%prepare_yambo_externals &&\
tar -xf %{SOURCE2}  --strip-components 1 -C external/devxlib/ &&\
tar -xf %{SOURCE3}  --strip-components 1 -C external/d3q/ &&\
tar -xf %{SOURCE4}  --strip-components 1 -C external/fox/ &&\
tar -xf %{SOURCE5}  --strip-components 1 -C external/mbd/ &&\
tar -xf %{SOURCE6}  --strip-components 1 -C external/pw2qmcpack/ &&\
tar -xf %{SOURCE7}  --strip-components 1 -C external/qe-gipaw/ &&\
tar -xf %{SOURCE8}  --strip-components 1 -C external/wannier90/ &&\
tar -xf %{SOURCE9}  --strip-components 1 -C external/want/ &&\
tar -xf %{SOURCE10} --strip-components 1 -C external/yambo/ &&\
cp -a external/yambo_externals/* external/yambo/lib/archive/ &&\
patch -i%{PATCH2} -p1 -dexternal/d3q/ &&\
patch -i%{PATCH3} -p1 -dexternal/yambo/ &&\
for f in $(find external/yambo/ -name '*.m4' -or -name 'configure'); do \
sed -i -e 's#\\(FC\\?UFLAGS=".*\\)"#\\1 -fPIC"#' "$f" \
sed -i -e 's#\\([ \\t]P\\?NETCDF_LIBS=".*\\)"#\\1 -lzip -lz -lm"#' "$f" \
done &&\
tar -xf external/yambo/lib/archive/hdf5-1.12.2.tar.gz --strip-components 1 -C external/hdf5/ &&\
cat external/mbd/src/mbd_version.f90.in | sed 's#@PROJECT_VERSION_MAJOR@#0#' | sed 's#@PROJECT_VERSION_MINOR@#12#' | sed 's#@PROJECT_VERSION_PATCH@#7#' | sed 's#@PROJECT_VERSION_SUFFIX@##' > external/mbd/src/mbd_version.f90 &&\
for f in $(grep -rl 'python$' external/wannier90/test-suite); do sed -i -e 's#bin/env python$#bin/env python3#' "$f"; done &&\
sed -i -e 's#maxter = 200#maxter = 300#' external/qe-gipaw/src/cgsolve_all.f90 &&\
cp -ar external/d3q         D3Q &&\
cp -ar external/qe-gipaw    GIPAW &&\
cp -ar external/wannier90   W90 &&\
cp -ar external/want        WANT &&\
cp -ar external/yambo       YAMBO

# -D__FFTW must be specified https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=980677
# Error: Symbol 'cft_2xy' at (1) has no IMPLICIT type
sed -i 's|MANUAL_DFLAGS  =|MANUAL_DFLAGS  = -D__FFTW %{extra_gfortran_flags}|' install/make.inc.in

# Allow for passing FOXFLAGS to external utils like fox or devicexlib
# relocation R_X86_64_32 against `.rodata' can not be used when making a PIE object; recompile with -fPIE
# Cannot compile fox without optimization due to
# #warning _FORTIFY_SOURCE requires compiling with optimization (-O)
# /usr/bin/ld: /tmp/ccy03rFL.ltrans0.ltrans.o:/builddir/build/BUILD/q-e-qe-7.0/PW/src/../../UtilXlib/fletcher32_mod.f90:216:
# more undefined references to `fletcher32' follow collect2: error: ld returned 1 exit status
sed -i 's|FOX_FLAGS = @foxflags@|FOX_FLAGS = $(FOXFLAGS)|' install/make.inc.in

# Horror! Tests use $HOME/tmp or /tmp by default!
sed -i 's#TMP_DIR=.*#TMP_DIR=./tmp#' environment_variables
sed -i 's#ESPRESSO_TMPDIR=.*#ESPRESSO_TMPDIR=./tmp#' test-suite/ENVIRONMENT
# NO network access during build!
sed -i 's#NETWORK_PSEUDO=.*#NETWORK_PSEUDO=/dev/null#' environment_variables
sed -i 's#NETWORK_PSEUDO=.*#NETWORK_PSEUDO=/dev/null#' test-suite/ENVIRONMENT
# must set ESPRESSO_ROOT explicitly
sed -i "s#ESPRESSO_ROOT=.*#ESPRESSO_ROOT=${PWD}#" test-suite/ENVIRONMENT
# set TESTCODE_NPROCS
sed -i "s#TESTCODE_NPROCS=.*#TESTCODE_NPROCS=2#" test-suite/ENVIRONMENT
# increase test verbosity
sed -i "s#--verbose#-vvv#" test-suite/Makefile
# bash uses source and not include
#sed -i "s#include #source #" test-suite/run-cp.sh
#sed -i "s#include #source #" test-suite/run-pw.sh
# don't use python2
#sed -i "s#python2#%%{python}#" test-suite/testcode/bin/testcode.py

# remove -D__XLF on ppc64
# http://qe-forge.org/pipermail/pw_forum/2009-January/085834.html
sed -i '/D__XLF/d' install/configure
# remove -D__LINUX_ESSL on ppc64
sed -i 's/try_dflags -D__LINUX_ESSL/try_dflags/' install/configure
sed -i 's/have_essl=1/have_essl=0/' install/configure


%build
# Have to do off-root builds to be able to build many versions at once
mv install install.orig

# To avoid replicated code define a macro
%global dobuild() \
mkdir -p bin$MPI_SUFFIX&& \
if [ "$MPI_SUFFIX" == "_serial" ]; then FORTRAN='gfortran'; CONFIGURE='--disable-parallel'; export MPI_LIBS=""; export SCALAPACK_LIBS="-lscalapack"; HDF5_OPT='--disable-parallel'; HDF5_CC='gcc'; fi&& \
if [ "$MPI_SUFFIX" == "_openmpi" ] && [ -r "$MPI_LIB/libmpi_f90.so" ]; then export LIBMPI='-lmpi -lmpi_f90 -lmpi_f77'; fi&& \
if [ "$MPI_SUFFIX" == "_openmpi" ] && [ -r "$MPI_LIB/libmpi_usempi.so" ]; then export LIBMPI='-lmpi -lmpi_usempi -lmpi_mpifh'; fi&& \
if [ "$MPI_SUFFIX" == "_openmpi" ] && [ -r "$MPI_LIB/libmpi_usempif08.so" ]; then export LIBMPI='-lmpi -lmpi_usempif08 -lmpi_mpifh'; fi&& \
if [ "$MPI_SUFFIX" == "_mpich2" ]; then export LIBMPI='-lmpich'; fi&& \
if [ "$MPI_SUFFIX" == "_mpich" ]; then export LIBMPI='-lmpich'; fi&& \
if [ "$MPI_SUFFIX" != "_serial" ]; then FORTRAN='mpif90'; CONFIGURE='--enable-parallel --with-scalapack=yes'; export MPI_LIBS="-L${MPI_LIB} $LIBMPI"; export SCALAPACK_LIBS="-L${MPI_LIB} -lscalapack"; HDF5_OPT='--enable-parallel'; HDF5_CC='mpicc'; fi&& \
    export CC=gcc &&\
    export CXX=c++ &&\
    export F90="${FORTRAN}" &&\
    export MPIF90="${FORTRAN}" &&\
    export FCFLAGS='%{optflags} %{extra_gfortran_flags}' &&\
    export CFLAGS='%{optflags} %{wnoflags} %{extra_gfortran_flags}' &&\
    export FFLAGS='%{optflags} %{extra_gfortran_flags}' &&\
    export FOXFLAGS='%{optflags} %{extra_gfortran_flags} -x f95-cpp-input' &&\
    export BLAS_LIBS='-l%{blaslib}' &&\
    export LAPACK_LIBS='-l%{blaslib}' &&\
    export FFT_LIBS='-lfftw3' &&\
    export HDF5_PATH=$(pwd)/hdf5 &&\
    pushd external/hdf5 &&\
    ./configure --prefix=${HDF5_PATH} --libdir=${HDF5_PATH}/%{_lib} --enable-fortran --disable-shared --enable-static %{WPICFLAG} --disable-cxx ${HDF5_OPT} --enable-build-mode=production CC=${HDF5_CC} && make && make install && \
    popd &&\
    %{_configure} $CONFIGURE %{WPICFLAG} --with-hdf5-libs="-L${HDF5_PATH}/%{_lib} -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -I${HDF5_PATH}/include" --with-hdf5-include="$(HDF5_PATH)/include" && \
    if [[ "$MPI_SUFFIX" != "_serial" ]]; then add_targets="d3q"; else add_targets=""; fi &&\
    %{__make} all all_currents couple epw gipaw $add_targets want yambo &&\
    pushd %{w90_path} &&\
    %{__make} all &&\
    popd &&\
    pushd YAMBO &&\
    %{__make} all &&\
    popd &&\
    for f in bin/*; do BASENAME=$(basename ${f}); cp -npL $f bin$MPI_SUFFIX/${BASENAME}; done&& \
    if test -d upftools; then for f in upftools/*.x; do BASENAME=$(basename ${f}); cp -npL $f bin$MPI_SUFFIX/${BASENAME}; done; fi&& \
    for f in %{w90_path}/*.x %{w90_path}/utility/w90vdw/w90vdw.x YAMBO/lib/iotk/iotk/bin/iotk.x; do if test -e $f; then BASENAME=$(basename ${f}); cp -npL $f bin$MPI_SUFFIX/${BASENAME}; fi; done &&\
    for f in %{w90_path}/utility/w90pov/w90pov YAMBO/bin/*; do if test -e $f; then BASENAME=$(basename ${f}); cp -npL $f bin$MPI_SUFFIX/${BASENAME}.x; fi; done &&\
    for f in WANT/bin/*; do BASENAME=$(basename ${f}); cp -npL $f bin$MPI_SUFFIX/${BASENAME}; done&& \
    %{__make} clean


# build openmpi version
cp -rp install.orig install
%prepare_externals
%{_openmpi_load}
%dobuild
%{_openmpi_unload}
rm -rf install

# build mpich version
cp -rp install.orig install
%prepare_externals
%{_mpich_load}
%dobuild
%{_mpich_unload}
rm -rf install

# build serial version
cp -rp install.orig install
%prepare_externals
MPI_SUFFIX=_serial %dobuild


%install

%global duplicate_execs pw.x manypw.x dist.x
# To avoid replicated code define a macro
%global doinstall() \
mkdir -p $RPM_BUILD_ROOT/$MPI_BIN&& \
mkdir -p $RPM_BUILD_ROOT/$MPI_LIB&& \
mkdir -p $RPM_BUILD_ROOT/$MPI_FORTRAN_MOD_DIR&& \
for f in bin$MPI_SUFFIX/*.x; do \
BASENAME=$(basename ${f})&& \
install -p -m 755 ${f} $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}_binary${EXE_SUFFIX}&& \
echo '#!/bin/bash' > $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}${EXE_SUFFIX}&& \
echo 'export FLEXIBLAS=openblas-serial' >> $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}${EXE_SUFFIX}&& \
echo -n "${BASENAME}_binary${EXE_SUFFIX} " >> $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}${EXE_SUFFIX}&& \
echo '"$@"' >> $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}${EXE_SUFFIX}&& \
chmod 755 $RPM_BUILD_ROOT/$MPI_BIN/${BASENAME}${EXE_SUFFIX}; done&& \
install -p -m 755 bin$MPI_SUFFIX/iotk $RPM_BUILD_ROOT/$MPI_BIN/iotk${EXE_SUFFIX}&& \
sed -i -e 's#iotk\\.x#iotk.x_binary'${EXE_SUFFIX}'#g' $RPM_BUILD_ROOT/$MPI_BIN/iotk${EXE_SUFFIX}&& \
install -p -m 755 bin$MPI_SUFFIX/sax2qexml $RPM_BUILD_ROOT/$MPI_BIN/sax2qexml${EXE_SUFFIX}&& \
sed -i -e 's#sax2qexml\\.x#sax2qexml.x_binary'${EXE_SUFFIX}'#g' $RPM_BUILD_ROOT/$MPI_BIN/sax2qexml${EXE_SUFFIX}&& \
chmod 755 $RPM_BUILD_ROOT/$MPI_BIN/iotk${EXE_SUFFIX} $RPM_BUILD_ROOT/$MPI_BIN/sax2qexml${EXE_SUFFIX}&& \
pushd $RPM_BUILD_ROOT/$MPI_BIN&& \
rm -f manypw.x_binary${EXE_SUFFIX} dist.x_binary${EXE_SUFFIX}&& \
ln -s pw.x_binary${EXE_SUFFIX} dist.x_binary${EXE_SUFFIX}&& \
ln -s pw.x_binary${EXE_SUFFIX} manypw.x_binary${EXE_SUFFIX}&& \
popd&& \
ls -al $RPM_BUILD_ROOT/$MPI_BIN

# install openmpi version
%{_openmpi_load}
EXE_SUFFIX=$MPI_SUFFIX %doinstall
%{_openmpi_unload}

# install mpich version
%{_mpich_load}
EXE_SUFFIX=$MPI_SUFFIX %doinstall
%{_mpich_unload}

# install serial version
EXE_SUFFIX="" MPI_SUFFIX="_serial" MPI_BIN=%{_bindir} MPI_LIB=%{_libdir} MPI_FORTRAN_MOD_DIR=%{_fmoddir} %doinstall


%check

# clean removes all extra pseudo - must copy them now
tar zxf %{SOURCE1}

%if 0%{?el6}
export TIMEOUT_OPTS='3600'
%else
export TIMEOUT_OPTS='--preserve-status --kill-after 10 3600'
%endif

# To avoid replicated code define a macro
%global docheck() \
export FLEXIBLAS=openblas-serial&& \
ldd bin$MPI_SUFFIX/pw.x && \
if [[ -d test-suite ]]; then rm -rf test-suite; fi && \
cp -rp test-suite.orig test-suite&& \
pushd test-suite&& \
for script in run-*.sh; do \
sed -i "s<}/bin/<}/bin$MPI_SUFFIX/<" ${script}&& \
sed -i "s<}/PW/src/<}/bin$MPI_SUFFIX/<" ${script}; \
done&& \
if [ $MPI_SUFFIX == _serial ]; then \
timeout ${TIMEOUT_OPTS} %{__make} run-tests-serial 2>&1 | tee ../tests$MPI_SUFFIX.log \
else \
timeout ${TIMEOUT_OPTS} %{__make} run-tests-parallel 2>&1 | tee ../tests$MPI_SUFFIX.log \
fi&& \
popd&& \
cat test-suite/pw_atom/test* && \
sync && sleep 15 && \
rm -rf test-suite

mv test-suite test-suite.orig

# check serial version
MPI_SUFFIX=_serial %docheck

# check openmpi version
%{_openmpi_load}
which mpirun
%docheck
%{_openmpi_unload}

# check mpich version
%{_mpich_load}
which mpirun
%docheck
%{_mpich_unload}

# restore tests
mv test-suite.orig test-suite


%files
%license License
%{_bindir}/*


%files openmpi
%license License
%{_libdir}/openmpi%{?_opt_cc_suffix}/bin/*


%files mpich
%license License
%{_libdir}/mpich%{?_opt_cc_suffix}/bin/*


%changelog
* Sat Nov 11 2023 L <lunusvir@gmail.com> - 7.3dev405-2
- Update to development version
- Build hdf5
- Patch d3q and wannier90
- Increase gipaw - cgsolve_all - max iteration to 300
- Workaround for infinite recursion in yambo build
- Fix "relocation R_X86_64_32 against .rodata" by adding -fPIE to FFLAGS

* Sun Jan 30 2022 Marcin Dulak <marcindulak@fedoraproject.org> - 7.0-3
- Fix "relocation R_X86_64_32 against .rodata" by passing -fPIE to FOXFLAGS
- Workaround for segmentation fault with gfortran-12 -fno-lto, bug #2046933

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Marcin Dulak <marcindulak@fedoraproject.org> - 7.0-1
- New upstream release

* Fri Aug 06 2021 Marcin Dulak <marcindulak@fedoraproject.org> - 6.8-1
- New upstream release
- Change changelog email
- Bundle gitlab.com/max-centre/components/devicexlib
- Remove no longer needed DEXX
- Remove no longer needed iotk
- Remove missing --with-elpa=no
- Export environment variables before configure
- Disable epel7 due to unsupported gfortran < 4.9
- export FLEXIBLAS=openblas-serial using a wrapper
- Remove empty devel and static packages

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 28 2020 Iñaki Úcar <iucar@fedoraproject.org> - 6.5-4
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 02 2020 Marcin Dulak <marcindulak@fedoraproject.org> - 6.5-2
- python and numpy br for epel8

* Fri Feb 14 2020 Marcin Dulak <marcindulak@fedoraproject.org> - 6.5-1
- new upstream release
- -fallow-argument-mismatch fix for gfortran 10
- fix serial and parallel test-suite build (use 1 and 2 processors respectively)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Marcin Dulak <marcindulak@fedoraproject.org> - 6.4.1-1
- new upstream release
- kill hanging tests after timeout
- disable failed architectures: configure fails to find openblas, fftw on other %%{openblas_arches} than x86_64 %%{ix86}

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 5.4.0-20
- Rebuild for openmpi 3.1.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 5.4.0-17
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 5.4.0-16
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 5.4.0-11
- Rebuild for openmpi 2.0

* Fri Sep 16 2016 Marcin Dulak <marcindulak@fedoraproject.org> - 5.4.0-10
- upsteam update
- speedup the tests by running on single core so koji %%{arm} builds finish within the timeout (bug #1356620)
- get rid of D__XLF and D__LINUX_ESSL on ppc64

* Tue Sep  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.3.0-9
- Sync openblas ExclusiveArch

* Thu Feb 18 2016 Marcin Dulak <marcindulak@fedoraproject.org> - 5.3.0-8
- use only 2 cores for tests (bug #1308481)
- defattr removed

* Sat Feb 13 2016 Marcin Dulak <marcindulak@fedoraproject.org> - 5.3.0-7
- explicit Requires are needed for scalapack, blacs on el6 (bug #1301922)
    
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Marcin Dulak <marcindulak@fedoraproject.org> 5.3.0-5
- upsteam update
- switch to test-suite
- no more upftools?

* Mon Jan  4 2016 Marcin Dulak <marcindulak@fedoraproject.org> 5.2.1-4
- disable compilation warnings
- use lua for copying pseudos
- removed common package

* Sat Dec 19 2015 Marcin Dulak <marcindulak@fedoraproject.org> 5.2.1-3
- fix ExclusiveArch
- license is GPLv2+
- OMP_NUM_THREADS removed
- use %%{optflags}

* Fri Dec 18 2015 Dave Love <loveshack@fedoraproject.org> - 5.2.1-2
- Require %%{name}-common, not %%{name}-common%%{?_isa}

* Wed Dec 16 2015 Marcin Dulak <marcindulak@fedoraproject.org> 5.1.2-1
- initial build

