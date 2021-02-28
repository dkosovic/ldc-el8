%global dmdfe_major 2
%global dmdfe_minor 0
%global dmdfe_bump  95
%global dmdfe       %dmdfe_major.%dmdfe_minor.%dmdfe_bump

#global pre beta1

%global llvm_version 11

# bootstrap_stage1 is for bringing up a D compiler for the very first time,
# without having a working D compiler in the build root.
%global bootstrap_stage1 0
%global bootstrap_stage1_ldc_version 0.17.6

# bootstrap_stage2 is for updating LDC to a newer version: it relies on an
# older, working LDC compiler in the buildroot, which is then used to build a
# new intermediate LDC version, and finally this in turn is used to build the
# final compiler that gets installed in the rpm.
%global bootstrap_stage2 0

%undefine _hardened_build

Name:           ldc
Epoch:          1
Version:        1.25.1%{?pre:~%{pre}}
Release:        1%{?dist}
Summary:        LLVM D Compiler

# The DMD frontend in dmd/* GPL version 1 or artistic license
# The files gen/asmstmt.cpp and gen/asm-*.hG PL version 2+ or artistic license
License:        BSD
URL:            https://github.com/ldc-developers/ldc
Source0:        https://github.com/ldc-developers/ldc/releases/download/v%{version}%{?pre:-%{pre}}/%{name}-%{version}%{?pre:-%{pre}}-src.tar.gz
%if 0%{?bootstrap_stage1}
Source1:        https://github.com/ldc-developers/ldc/releases/download/v%{bootstrap_stage1_ldc_version}/%{name}-%{bootstrap_stage1_ldc_version}-src.tar.gz
%endif
Source3:        macros.%{name}

# Make sure /usr/include/d is in the include search path
Patch0:         ldc-include-path.patch

ExclusiveArch:  %{ldc_arches}

BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  gc
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if ! 0%{?bootstrap_stage1}
BuildRequires:  ldc
%endif
BuildRequires:  libconfig-devel
BuildRequires:  libcurl-devel
BuildRequires:  libedit-devel
BuildRequires:  llvm%{?llvm_version}-devel
BuildRequires:  llvm%{?llvm_version}-static
BuildRequires:  make
BuildRequires:  zlib-devel

# Require gcc for linking
Requires:       gcc

# Removed in F33
Obsoletes:      ldc-druntime-devel < 1:1.23.0
Obsoletes:      ldc-jit-devel < 1:1.23.0
Obsoletes:      ldc-phobos-devel < 1:1.23.0

%description
LDC is a portable compiler for the D programming language with modern
optimization and code generation capabilities.

It uses the official DMD compiler frontend to support the latest version
of D, and relies on the LLVM Core libraries for code generation.

%package        druntime
Summary:        Runtime library for D
License:        Boost

%description druntime
Druntime is the minimum library required to support the D programming
language. It includes the system code required to support the garbage
collector, associative arrays, exception handling, array vector operations,
startup/shutdown, etc.

%description druntime -l fr
Druntime est la bibliothèque minimal requise pour supporter la programmation en
D. Est inclut le code système requis pour supporter le ramasse miette, tableau
associatif, gestion des exceptions, opertation sur des vecteurs,
démarage/extinction, etc

%package        jit
Summary:        LDC JIT library
License:        Boost

%description jit
JIT library for the LDC compiler.

%package        phobos
Summary:        Standard Runtime Library
License:        Boost
Requires:       %{name}-druntime%{?_isa} = %{epoch}:%{version}-%{release}

%description phobos
Each module in Phobos conforms as much as possible to the following design
goals. These are goals rather than requirements because D is not a religion,
it's a programming language, and it recognizes that sometimes the goals are
contradictory and counterproductive in certain situations, and programmers have
jobs that need to get done

%description phobos -l fr
Chaque module de Phobos est conforme autant que possible à la conception
suivante objectifs. Ce sont des objectifs plutôt que des exigences car D n'est
pas une religion, c'est un language de programmation, et il reconnaît que,
parfois, les objectifs sont contradictoires et contre-productif dans certaines
situations, et les programmeurs ont travail qui doit être effectué.

%package phobos-geany-tags
Summary:        Support for enable autocompletion in geany
Requires:       %{name} = %{epoch}:%{version}-%{release}
BuildArch:      noarch
BuildRequires:  geany
Requires:       geany

%description phobos-geany-tags
Enable autocompletion for phobos library in geany (IDE)

%description -l fr phobos-geany-tags
Active l'autocompletion pour pour la bibliothèque phobos dans geany (IDE)

%prep
%autosetup -n %{name}-%{version}%{?pre:-%{pre}}-src -p1
# temp geany config directory for allow geany to generate tags
mkdir geany_config

%build
# This package appears to be failing because links to the LLVM plugins
# are not installed which results in the tools not being able to
# interpret the .o/.a files.  Disable LTO for now
%define _lto_cflags %{nil}

%global optflags %{optflags} -fno-strict-aliasing

%if 0%{?bootstrap_stage1}
tar xf %{SOURCE1}
mkdir build-bootstrap1
pushd build-bootstrap1
cmake -DLLVM_CONFIG:PATH=%{_bindir}/llvm-config-%{?llvm_version:%{llvm_version}-}%{__isa_bits} \
      ../%{name}-%{bootstrap_stage1_ldc_version}-src
make %{?_smp_mflags}
popd
%endif

%if 0%{?bootstrap_stage2}
tar xf %{SOURCE0}
mkdir build-bootstrap2
pushd build-bootstrap2
cmake -DLLVM_CONFIG:PATH=%{_bindir}/llvm-config-%{?llvm_version:%{llvm_version}-}%{__isa_bits} \
%if 0%{?bootstrap_stage1}
      -DD_COMPILER:PATH=`pwd`/../build-bootstrap1/bin/ldmd2 \
%endif
      ../%{name}-%{version}%{?pre:-%{pre}}-src
make %{?_smp_mflags}
popd
%endif

%cmake -DMULTILIB:BOOL=OFF \
       -DINCLUDE_INSTALL_DIR:PATH=%{_prefix}/lib/ldc/%{_target_platform}/include/d \
       -DBASH_COMPLETION_COMPLETIONSDIR:PATH=%{_datadir}/bash-completion/completions \
       -DLLVM_CONFIG:PATH=llvm-config-%{?llvm_version:%{llvm_version}-}%{__isa_bits} \
%if 0%{?bootstrap_stage2}
       -DD_COMPILER:PATH=`pwd`/build-bootstrap2/bin/ldmd2 \
%endif
       %{nil}

%cmake_build

# generate geany tags
geany -c geany_config -g phobos.d.tags $(find runtime/phobos/std -name "*.d")

%install
%cmake_install

# macros for D package
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install --mode=0644 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/macros.d/macros.ldc

# geany tags
mkdir -p %{buildroot}/%{_datadir}/geany/tags/
install -m0644 phobos.d.tags %{buildroot}/%{_datadir}/geany/tags/

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/ldc2.conf
%{_bindir}/ldc2
%{_bindir}/ldmd2
%{_bindir}/ldc-build-runtime
%{_bindir}/ldc-prune-cache
%{_rpmconfigdir}/macros.d/macros.ldc
%dir %{_prefix}/lib/ldc
%dir %{_prefix}/lib/ldc/%{_target_platform}
%dir %{_prefix}/lib/ldc/%{_target_platform}/include
%dir %{_prefix}/lib/ldc/%{_target_platform}/include/d
%{_prefix}/lib/ldc/%{_target_platform}/include/d/core
%{_prefix}/lib/ldc/%{_target_platform}/include/d/etc
%{_prefix}/lib/ldc/%{_target_platform}/include/d/ldc
%{_prefix}/lib/ldc/%{_target_platform}/include/d/object.d
%{_prefix}/lib/ldc/%{_target_platform}/include/d/std
%{_libdir}/libdruntime-ldc-debug-shared.so
%{_libdir}/libdruntime-ldc-shared.so
%{_libdir}/libldc-jit-rt.a
%{_libdir}/libldc-jit.so
%{_libdir}/libphobos2-ldc-debug-shared.so
%{_libdir}/libphobos2-ldc-shared.so
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/ldc2

%files jit
%license runtime/phobos/LICENSE_1_0.txt
%{_libdir}/libldc-jit.so.%dmdfe
%{_libdir}/libldc-jit.so.%dmdfe_bump

%files druntime
%license runtime/druntime/LICENSE.txt
%doc runtime/druntime/README.md runtime/README
%{_libdir}/libdruntime-ldc-debug-shared.so.%dmdfe
%{_libdir}/libdruntime-ldc-debug-shared.so.%dmdfe_bump
%{_libdir}/libdruntime-ldc-shared.so.%dmdfe
%{_libdir}/libdruntime-ldc-shared.so.%dmdfe_bump

%files phobos
%license runtime/phobos/LICENSE_1_0.txt
%{_libdir}/libphobos2-ldc-debug-shared.so.%dmdfe
%{_libdir}/libphobos2-ldc-debug-shared.so.%dmdfe_bump
%{_libdir}/libphobos2-ldc-shared.so.%dmdfe
%{_libdir}/libphobos2-ldc-shared.so.%dmdfe_bump

%files phobos-geany-tags
%{_datadir}/geany/tags/phobos.d.tags

%changelog
* Sun Feb 28 2021 Kalev Lember <klember@redhat.com> - 1:1.25.1-1
- Update to 1.25.1

* Sun Feb 21 2021 Kalev Lember <klember@redhat.com> - 1:1.25.0-1
- Update to 1.25.0
- Build with llvm 11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 21 2020 Kalev Lember <klember@redhat.com> - 1:1.23.0-1
- Update to 1.23.0
- Merge -devel subpackages into the main ldc package
- Move ldc internal headers to /usr/lib/ldc to avoid conflicting with gdc (#1781685)

* Fri Aug 21 2020 Kalev Lember <klember@redhat.com> - 1:1.20.1-5
- Explicitly build against llvm10 compat package
- Fix FTBFS with new cmake macros on F33 (#1863964)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.20.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Mar 07 2020 Jeff Law <law@redhat.com> - 1:1.20.1-2
- Disable LTO

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 1:1.20.1-1
- Update to 1.20.1

* Sat Feb 15 2020 Kalev Lember <klember@redhat.com> - 1:1.20.0-2
- Update to 1.20.0 final release
- Build with llvm 10.0

* Tue Feb 11 2020 Kalev Lember <klember@redhat.com> - 1:1.20.0-1.beta1
- Update to 1.20.0 beta1

* Mon Feb 10 2020 Kalev Lember <klember@redhat.com> - 1:1.19.0-1
- Update to 1.19.0
- Build with llvm 9.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 08 2019 Kalev Lember <klember@redhat.com> - 1:1.15.0-1
- Update to 1.15.0
- Build with llvm 8.0

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 1:1.14.0-3
- Disable bootstrap

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 1:1.14.0-2
- Enable bootstrap

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 1:1.14.0-1
- Update to 1.14.0
- Add stage2 bootstrap for doing stage2 build with the same compiler

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 14 2018 Kalev Lember <klember@redhat.com> - 1:1.12.0-2
- Disable bootstrap

* Sat Oct 13 2018 Kalev Lember <klember@redhat.com> - 1:1.12.0-1
- Update to 1.12.0
- Enable bootstrap
- Update bootstrap compiler to ldc 0.17.6

* Mon Aug 20 2018 Kalev Lember <klember@redhat.com> - 1:1.11.0-2
- Disable bootstrap

* Sun Aug 19 2018 Kalev Lember <klember@redhat.com> - 1:1.11.0-1
- Update to 1.11.0
- Update bootstrap compiler to latest git snapshot
- Build with llvm 6.0
- Bootstrap on aarch64

* Mon Jul 16 2018 Kalev Lember <klember@redhat.com> - 1:1.11.0-0.4.beta2
- Require gcc for linking

* Mon Jul 16 2018 Kalev Lember <klember@redhat.com> - 1:1.11.0-0.3.beta2
- Update to 1.11.0 beta2
- Disable bootstrap

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Kalev Lember <klember@redhat.com> - 1:1.11.0-0.1.beta1
- Update to 1.11.0 beta1

* Wed Jun 20 2018 Kalev Lember <klember@redhat.com> - 1:1.10.0-1
- Update to 1.10.0
- Enable bootstrap
- Update bootstrap compiler to ldc 0.17.6 git snapshot

* Mon Mar 19 2018 Tom Stellard <tstellar@redhat.com> - 1:1.8.0-2
- Rebuild for LLVM 6.0.0 and re-enable JIT libraries.

* Sun Mar 04 2018 Kalev Lember <klember@redhat.com> - 1:1.8.0-1
- Update to 1.8.0

* Mon Feb 19 2018 Kalev Lember <klember@redhat.com> - 1:1.8.0-0.2.beta1
- Disable bootstrap

* Mon Feb 19 2018 Kalev Lember <klember@redhat.com> - 1:1.8.0-0.1.beta1
- Update to 1.8.0 beta1
- Enable bootstrap
- Build against llvm 4.0
- Disable strict aliasing
- Use ldconfig_scriptlets macro

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 26 2017 Tom Stellard <tstellard@redhat.com> - 1:1.4.0-3
- Fix build with LLVM 5.0

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 1:1.4.0-2
- Disable bootstrap

* Tue Sep 12 2017 Kalev Lember <klember@redhat.com> - 1:1.4.0-1
- Update to 1.4.0
- Enable bootstrap

* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-4
- Tighten subpackage deps

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-1
- Update to 1.3.0

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-0.4.beta2
- Don't require base ldc package for ldc-druntime and ldc-phobos

* Tue Jun 13 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-0.3.beta2
- Reduce optimization level from -O3 to work around ldc crashes

* Tue Jun 13 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-0.2.beta2
- Disable bootstrap

* Tue Jun 13 2017 Kalev Lember <klember@redhat.com> - 1:1.3.0-0.1.beta2
- Update to 1.3.0 beta2
- Enable bootstrap
- Update bootstrap compiler to ldc 0.17.4

* Thu May 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.1.1-4
- Rebuild llvm-4

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Thu Mar 30 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:1.1.1-2
- Rebuild for LLVM4

* Fri Mar 03 2017 Kalev Lember <klember@redhat.com> - 1:1.1.1-1
- Update to 1.1.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Kalev Lember <klember@redhat.com> - 1:1.1.0-2
- Disable bootstrap

* Fri Jan 27 2017 Kalev Lember <klember@redhat.com> - 1:1.1.0-1
- Update to 1.1.0
- Enable bootstrap
- Merge -config subpackage into the main ldc package
- Don't mark the rpm macros file and bash completion file as config
- Avoid depending on bash-completion
- Use license macro for license files

* Tue Dec 13 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.7.beta6
- Update to 1.1.0 beta6

* Wed Nov 30 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.6.beta4
- Disable bootstrap

* Wed Nov 30 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.5.beta4
- Backport a patch to fix PPC/PPC64 ABI issues

* Sun Nov 27 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.4.beta4
- Update to 1.1.0 beta4
- Enable bootstrap

* Tue Nov 01 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.3.beta3
- Disable bootstrap

* Tue Nov 01 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.2.beta3
- Revert bundled zlib removal as this broke libphobos2-ldc (#1102856)

* Mon Oct 31 2016 Kalev Lember <klember@redhat.com> - 1:1.1.0-0.1.beta3
- Update to 1.1.0 beta3
- Add a bootstrap build option; enable bootstrap
- Remove bundled zlib (#1102856)

* Mon Oct 31 2016 Kalev Lember <klember@redhat.com> - 1:0.17.2-3
- Move ldc_arches macro to redhat-rpm-config

* Sun Oct 30 2016 Kalev Lember <klember@redhat.com> - 1:0.17.2-2
- Add ldc_arches macro that other packages can use
- Enable ppc64 and ppc64le architectures

* Sun Oct 16 2016 Kalev Lember <klember@redhat.com> - 1:0.17.2-1
- Update to 0.17.2
- Enable arm architecture

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.16.1-78
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.16.1-77
- Update ldc to latest stable release

* Fri Sep 18 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.16.0.alpha2-76
- update to beta release 0.16.0-alpha3

* Fri Sep 18 2015 Jonathan MERCIER <bioinfornatics@gmail.com>
- update to beta release 0.16.0-alpha3

* Fri Sep 18 2015 Jonathan MERCIER <bioinfornatics@gmail.com>
- update to beta release 0.16.0-alpha3

* Sun Sep 06 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.16.0.alpha2-73
- update to release 0.16.2-alpha2

* Thu Jul 30 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.15.2.beta2-72
- add bash-completion as required

* Wed Jul 29 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.15.2.beta2-71
- update to beta release 0.15.2-beta2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.15.2.beta1-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:0.15.2.beta1-69
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 31 2015 bioinfornatics@gmail.com - 1:0.15.2.beta1-68
- rebuild

* Fri Mar 20 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.15.2.beta1-66
- update to beta release 0.15.2

* Sun Feb 01 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.15.1-65
- update to version 0.15.1

* Sun Feb 01 2015 Jonathan MERCIER <bioinfornatics@gmail.com> - 1:0.15.0-64
- fix spec missing libedit

* Thu Oct 30 2014 Jonathan MERCIER <bioinfornatics@gmail.com> - 0.15.0-alpha1-63
- update to 0.15 alpaha 1 release
- enable epoch to follow upstream version number 2 become 0.15

* Sun Sep 14 2014 bioinfornatics - 0.14.0-62
- Update LDC to release 0.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 0.13.0-59
- update to latest rev

* Sun Apr 27 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2-58.20140325git7492d06
- update to latest rev

* Mon Mar 10 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2-57.20140305git6e908ff
- Add config sub-package
- put rpm macro into %%{_rpmconfigdir}/macros.d

* Sun Mar 09 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2-56.20140305git6e908ff
- Fix alphatag

* Sat Mar 08 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2-55.20131023git287e089
- Update to rev 6e908ff

* Thu Oct 24 2013 Jonathan MERCIER <bioinfornatics@gmail.com> - 2-54.20131023git287e089
- Update to rev 287e089

* Fri Aug 09 2013 Jonathan MERCIER <bioinfornatics@gmail.com> - 2-53.20130805git967b986
- Add ExcludeArch arm

* Mon Aug 05 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2-52.20130805git967b986
- Update to rev 967b986

* Sun Aug 04 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2-51.20130730git07cb4cc
- Update to rev 07cb4cc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-50.20130623git9facd25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-49.20130623git9facd25
- Update url  and add macros.ldc into git repo

* Mon Jun 24 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-48.20130623git9facd25
- Add phobos and druntimeas as ldc's require

* Sun Jun 23 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-47.20130623git9facd25
- Update to rev 9facd25

* Tue Jun 11 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-46.20130611git39637c8
- Update to rev 39637c8

* Tue Jun 11 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-45.20130610git354e271
- Update to rev 354e271

* Mon Jun 10 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-44.20130610gitbf0e03d
- Update to rev bf0e03d

* Sun Jun 09 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-43.20130607gitf7aac52
- Update to rev f7aac52

* Fri May 24 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-42.20130519git6e57b6c
- Update to rev 6e57b6c

* Sat May 18 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-41.20130513git23df06a
- Fix zlib require

* Sat May 18 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-40.20130513git23df06a
- Fix bogus date

* Fri May 17 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-39.20130513git23df06a
- add zlib as build require

* Fri May 17 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-38.20130513git23df06a
- bump

* Fri May 17 2013 Jonathan MERCIER <bioinfornatics at fedoraproject dot org> - 2-37.20130513git23df06a
- bump

* Wed May 15 2013  <bioinfornatics at fedoraproject dot org> - 2-36.20130513git23df06a
- Update to rev 23df06a

* Fri May 10 2013 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-35.20130510git91d653c
- Update to rev 91d653c

* Thu May 09 2013 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-34.20130509git8f26877
- Update to rev 8f26877

* Thu May 09 2013 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-33.20130506git51e1a6c
- Update to rev 51e1a6c

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-32.20121007git0777102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-31.20121007git0777102
- Update to latest revision

* Wed Oct 03 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-30.20121003gitb8e62b8
- update ldc to rev b8e62b8

* Wed Sep 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-29.20120921git8968103
- ldc own D include dir
- Update to dmdfe 2.060

* Sat Aug 11 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-28.20120811git34d595d
- Update ldc

* Thu Jul 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-27.20120720git5f15b30
- fix link against libcurl

* Sun Jul 22 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-26.20120624gitcef19fb
- Update to use llvm 3.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-15.201210307git43667e1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-24.20120624gitcef19fb
- Fix doc generation bug

* Mon Jun 25 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-23.20120624gitcef19fb
- update ldc

* Fri Jun 15 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-22.20120613git3eef7b7
- update ldc

* Wed Jun 06 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-21.20120606git1c301aa
- fix imported di file

* Sun Jun 03 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-18.20120602git260faae
- remove buildroot path into .di file

* Sat Jun 02 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-17.20120602gitd24592b
- fix bug to able tango build bis

* Sat Jun 02 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-16.20120602git509a579
- fix bug to able tango build

* Fri May 25 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-15.20120525git1805e53
- update to latest rev dmdfe 2.059

* Mon Mar 12 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-14.201210307git43667e1
- update to latest rev

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-13.201210215git5af48ed
- Rebuilt for c++ ABI breakage

* Sat Feb 18 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-12.201210218git53f9964
- Update to latest revision
- update dmdfe to 2.058
- ldc has new parameter -soname
- fix library creation when multiple object files
- fix phobos and druntime soname

* Mon Feb 13 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2-11.201210207git72d510c
- update to latest revision
- update dmdfe to 2.057
- fix tango build for 32 bit

* Thu Jan 05 2012 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-10.20111206gitfa5fb92
- fix doc for devhelp

* Fri Dec 09 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-9.20111206gitfa5fb92
- Add doc for devhelp

* Tue Dec 06 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-8.20111206gitfa5fb92
- Put %%{_d_includedir}/core into druntime-devel package

* Tue Dec 06 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-8.20111206git641cc85
- Update compiler to latest revision
- Update runtime to latest revision
- Update phobos to latest revision

* Thu Dec 01 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-7.20111117git4add11b
- Update to latest revision
- fix dependencies

* Wed Nov 09 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-6.20111112gitd9da872
- Update to latest revision

* Wed Nov 09 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-5.20110911git3cf958ad
- Update to latest revision

* Sat Sep 17 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-4.20110915git423076d
- Update to latest revision

* Wed Aug  03 2011 Michel Salim <salimma@fedoraproject.org> - 2-3.20110801git58d40d2
- Rebuild against final LLVM 2.9 release

* Mon Aug  01 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-2.20110801git58d40d2
- update LDC2 from upstream

* Tue Jul 26 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-2.20110826hg1991
- update LDC2 from upstream

* Sun Mar 06 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-1.20110615hg1965
- update to LDC2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-31.20110115hg1832
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-30.20110115hg1832
update to latest revision 1832

* Fri Jan 07 2011 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-29.20110110hg1828
update to latest revision 1828

* Fri Jan 07 2011 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-28.20110105hg1812
update to latest revision 1812

* Wed Jan 05 2011 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-27.20110102hg1705
- update to latest revision 1705

* Sun Nov 14 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-25.20101114hg1698
- update to latest revision 1698
- several bug fix

* Wed Oct 20 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-23.20101004hg1666
- add patch for llvm 2.8

* Fri Oct 15 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-22.20101004hg1666
- update to new release 1666

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-21.20100928hg1665
- update to new release 1665

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-20.20100927hg1664
- update to new release 1664

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-19.20100905hg1659
- update to new release 1659

* Sat Sep 04 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-18.20100904hg1657
- update to new release 1657

* Thu Aug 26 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-17.20100609hg1655
- use %%{_libdir} instead %%{_libdir}/d

* Thu Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-16.20100609hg1655
- fix minor bug in /etc/ldc.conf

* Thu Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-15.20100609hg1655
- fix minor bug in /etc/ldc.conf

* Thu Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-14.20100609hg1655
- fix critical bug in /etc/ldc.conf

* Wed Aug 11 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-13.20100609hg1655
- fix critical bug in /etc/ldc.conf

* Sat Aug 07 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-12.20100609hg1655
- Update to revision 1655

* Mon Aug 02 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-12.20100609hg1654
- Add patch

* Mon Aug 02 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-11.20100609hg1654
- Add %%{?_smp_mflags} macro for makefile
- Add flag -O2 for good optimizations in %%{_d_optflags} macro

* Sun Aug 01 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-10.20100609hg1654
- Update to revision 1654

* Thu Jul 29 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-9.20100609hg1653
- add %%{_d_libdir} macro in macros.ldc
- fix lib path in ldc.conf

* Wed Jul 28  2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-8.20100609hg1653
- Using macro for D package

* Tue Jul 27 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-7.20100609hg1653
- Fix macros.ldc name

* Tue Jul 27 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-6.20100609hg1653
- Add %%{_sysconfdir}/rpm/maco.ldc file for new macro
- Fix alphatag to YYYYMMDD instead YYYYDDMM

* Sun Jul 25 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-5.20100706hg1653
- Fix ldc.rebuild.conf file

* Thu Jul 15 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-4.20100706hg1653
- Add gcc in require

* Thu Jul 01 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-3.20100706hg1653
- Perform french description

* Thu Jun 24 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-2.20100706hg1653
- Explain why .emty file is removed

* Wed Jun 23 2010 Jonathan MERCIER <bioinfornatics at gmail.com> - 0.9.2-1.20100706hg1653
- Initial release
