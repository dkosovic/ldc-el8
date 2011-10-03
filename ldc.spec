<<<<<<< HEAD
%global     snapdate        20110915
%global     ldc_rev         423076d
%global     phobos_rev      a8106d9
%global     druntime_rev    fba10fa
%global     alphatag        %{snapdate}git%{ldc_rev}
%global     phobostag       %{snapdate}git%{phobos_rev}
%global     druntimetag     %{snapdate}git%{druntime_rev}

# The source for this package was pulled from upstream's git.
=======
%global     alphatag        20110801
# incorrect tarball name
%global     err_alphatag    20110901
%global     git_revision    git58d40d2

# The source for this package was pulled from upstream's subversion (svn).
>>>>>>> 554b45aa5499869ae1e69c821397ac3ff20cda11
# Use the following commands to generate the tarball:
# cd ldc; git rev-parse --short HEAD            -> for ldc_rev
# cd ldc/phobos; git rev-parse --short HEAD     -> for phobos_rev
# cd ldc/druntime/;  git rev-parse --short HEAD -> for druntime_rev
# git clone https://github.com/ldc-developers/ldc.git
# (cd ldc; git checkout 423076d; git submodule init; git submodule update; \
#  git archive --prefix=ldc-%%{alphatag}/ HEAD \
# ) | xz > ldc-%%{alphatag}.xz
# (cd ldc/druntime; \
#  git archive --prefix=druntime/ HEAD \
# ) | xz > ldc-druntime-%%{druntimetag}.xz
# (cd ldc/phobos; \
#  git archive --prefix=phobos/ HEAD \
# ) | xz > ldc-phobos-%%{phobostag}.xz

Name:           ldc
Version:        2
<<<<<<< HEAD
Release:        4.%{alphatag}%{?dist}
=======
Release:        3.%{alphatag}%{git_revision}%{?dist}
>>>>>>> 554b45aa5499869ae1e69c821397ac3ff20cda11
Summary:        A compiler for the D programming language

Group:          Development/Languages
# The DMD frontend in dmd/* GPL version 1 or artistic license
# The files gen/asmstmt.cpp and gen/asm-*.hG PL version 2+ or artistic license
License:        BSD    
URL:            http://www.dsource.org/projects/ldc
<<<<<<< HEAD
Source0:        %{name}-%{alphatag}.tar.xz
Source1:        %{name}-phobos-%{phobostag}.tar.xz
Source2:        %{name}-druntime-%{druntimetag}.tar.xz
Source3:        macros.%{name}
# fix current build system report to upstream done
Patch0:         %{name}_fix_build.patch
=======
Source0:        %{name}-%{err_alphatag}%{git_revision}.tar.xz
Source1:        macros.%{name}
>>>>>>> 554b45aa5499869ae1e69c821397ac3ff20cda11
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  llvm-devel >= 2.9
BuildRequires:  libconfig, libconfig-devel
BuildRequires:  cmake
BuildRequires:  gc, gcc-c++, gcc
BuildRequires:  llvm-devel

%description
LDC is a compiler for the D programming Language. It is based on the latest DMD
frontend and uses LLVM as backend. LLVM provides a fast and modern backend for
high quality code generation. LDC is released under a BSD license with
exceptions for the DMD frontend and code from GDC.
The development takes place mostly on x86-32 and x86-64 Linux and that is where
LDC works best. Support for other platforms and architectures is under
development, but we are still looking for people to help test and adjust LDC
for those platforms!
LDC already compiles a lot of D code, but should still be considered beta
quality. Take a look at the tickets to get a better impression on what still
needs to be implemented.

%description -l fr_FR
LDC est un compiler pour le langage de programmation D. Il est basé sur la
dernière, interface de DMD et utilise LLVM comme moteur. LLVM est un moteur
rapide pour la génération de code de haute qualité. LDC est publié sous licence
BSD avec des exception pour l'interfaces DMD et le code provenant de GDC.
Le développement se concentre surtout pour les architectures x86 et x86_64
sur Linux et c'est pour cela que LDC travaille bien. le support pour les autres
architectures et plateformes sont en développement, mais nous recherchons
des personnes pour aider au test et amélioré LDC pour ces plateformes.
LDC compile déjà une grande quantité de code D, mais doit encore être considéré
en qualité bêta. Regarder les tickets pour ressentir ce qui doit encore être
implémenter.

%package        druntime
Summary:        Runtime library for D
Group:          Development/Tools
License:        Boost
Requires:       %{name} =  %{version}-%{release}

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


%package        druntime-devel
Summary:        Support for developing D application
Group:          Development/Tools
Requires:       %{name} =  %{version}-%{release}


%description druntime-devel
The druntime-devel package contains header files for developing D
applications that use druntime.

%description druntime-devel -l fr
Le paquet druntime-devel contient les fichiers d'entêtes pour développer
des applications en D utilisant druntime.

%package        phobos
Summary:        Standard Runtime Library
Group:          Development/Tools
License:        Boost
Requires:       %{name} =  %{version}-%{release}
Requires:       %{name}-druntime

%description phobos
Each module in Phobos conforms as much as possible to the following design
goals. These are goals rather than requirements because D is not a religion,
it's a programming language, and it recognizes that sometimes the goals are
contradictory and counterproductive in certain situations, and programmers have
jobs that need to get done

%description phobos -l fr
Chaque module de Phobos est conforme autant que possible à la conception
suivante objectifs. Ce sont des objectifs plutôt que des exigences car D n'est
pas une religion, c'est un langage de programmation, et il reconnaît que,
parfois, les objectifs sont contradictoire et contre-productive dans certaines
situations, et les programmeurs doivent implémenter d'une certaines manière.

%package        phobos-devel
Summary:        Support for developing D application
Group:          Development/Tools
Requires:       %{name} =  %{version}-%{release}

%description phobos-devel
The phobos-devel package contains header files for developing D
applications that use phobos.

%description phobos-devel -l fr
Le paquet phobos-devel contient les fichiers d'entêtes pour développer
des applications en D utilisant phobos.

%prep
<<<<<<< HEAD
%setup -q -n %{name}-%{alphatag}
%setup -q -T -D -a 1 -n %{name}-%{alphatag}
%setup -q -T -D -a 2 -n %{name}-%{alphatag}
%patch0 -p1 -b .fix
find . -type f -exec sed -i 's/\r//g' {} \;
=======
%setup -q -n %{name}-%{err_alphatag}%{git_revision}
find . -type f -exec sed -i 's/\r//g' {} \;
# config.h is renamed in Fedora to allow for 32- and 64-bit llvm-devel to
# coexist; look for the appropriate file
sed -i.multilib -e 's|config.h|config-%{__isa_bits}.h|' CMakeLists.txt
#%patch0 -p1
>>>>>>> 554b45aa5499869ae1e69c821397ac3ff20cda11

%build
%cmake  -DD_VERSION:STRING=2                        \
        -DCONF_INST_DIR:PATH=%{_sysconfdir}         \
        -DRUNTIME_DIR=./druntime                    \
        -DPHOBOS2_DIR=./phobos                      \
        -DD_FLAGS:STRING="-O2;-g;-w;-d;-release"    \
        -DLLVM_CONFIG_HEADER=config-%{__isa_bits}.h \
        .
make  VERBOSE=2 phobos2

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}/%{_includedir}/d/ldc
install --mode=0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.ldc

sed -i \
    -e      "10a \ \ \ \ \ \ \ \"-I%{_includedir}\/d\","        \
    -e      "11a \ \ \ \ \ \ \ \"-I%{_includedir}\/d\/phobos\","\
    -e      "/^.*-I.*%{name}-%{alphatag}%{git_revision}.*$/d"   \
    -e      "s/-L-L.*lib/-L-L$(%{_libdir})\/druntime.so/"       bin/ldc2.conf 

sed -i "s|DFLAGS.*|DFLAGS=-I%{_includedir}/d -L-L%{_libdir} -d-version=Phobos -defaultlib=phobos2 -debuglib=phobos2|" bin/ldc2.rebuild.conf

ln %{buildroot}%{_bindir}/ldc2	%{buildroot}%{_bindir}/ldc

# fix install
    # lib for 64bits
%ifarch x86_64 sparc64
    mv %{buildroot}/%{_prefix}/lib %{buildroot}/%{_libdir}/
%endif

    # devel file
ls  %{buildroot}/%{_prefix}
mv %{buildroot}/%{_prefix}/src/debug/%{name}-%{alphatag} %{buildroot}/%{_includedir}/d/
rm -fr %{buildroot}/%{_includedir}/d/runtime
    # druntime
mv %{buildroot}/%{_includedir}/d/druntime/src/* %{buildroot}/%{_includedir}/d/druntime:
rm -fr %{buildroot}/%{_includedir}/d/druntime/src
    # phobos

    # ldc
mv %{buildroot}/%{_includedir}/d/dmd2   %{buildroot}/%{_includedir}/d/ldc/dmd2
mv %{buildroot}/%{_includedir}/d/gen    %{buildroot}/%{_includedir}/d/ldc/gen
mv %{buildroot}/%{_includedir}/d/ir     %{buildroot}/%{_includedir}/d/ldc/ir
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%config(noreplace)  %{_sysconfdir}/ldc2.rebuild.conf
%config(noreplace)  %{_sysconfdir}/ldc2.conf
%config             %{_sysconfdir}/rpm/macros.ldc
%{_bindir}/ldc
%{_bindir}/ldc2
%{_bindir}/ldmd2
%{_includedir}/d/ldc

%files druntime
%defattr(-,root,root,-)
%doc druntime/LICENSE_1_0.txt druntime/README.txt
%{_libdir}/libdruntime-ldc.so

%files druntime-devel
%defattr(-,root,root,-)
%{_includedir}/d/druntime
%{_includedir}/d/object.di

%files phobos
%defattr(-,root,root,-)
%doc phobos/LICENSE_1_0.txt
%{_libdir}/liblphobos2.so

%files phobos-devel
%defattr(-,root,root,-)
%{_includedir}/d/std
%{_includedir}/d/etc

%changelog
<<<<<<< HEAD
* Sat Sep 17 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-4.20110915git423076d
- Update to latest revision

=======
>>>>>>> 554b45aa5499869ae1e69c821397ac3ff20cda11
* Wed Aug  3 2011 Michel Salim <salimma@fedoraproject.org> - 2-3.20110801git58d40d2
- Rebuild against final LLVM 2.9 release

* Mon Aug  1 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-2.20110801git58d40d2
- update LDC2 from upstream

* Tue Jul 26 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-2.20110826hg1991
- update LDC2 from upstream

* Sun Mar 06 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 2-1.20110615hg1965
- update to LDC2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-31.20110115hg1832
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-30.20110115hg1832
 update to latest revision 1832
 
* Mon Jan 07 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-29.20110110hg1828
 update to latest revision 1828

* Fri Jan 07 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-28.20110105hg1812
 update to latest revision 1812

* Mon Jan 05 2011 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-27.20110102hg1705
- update to latest revision 1705

* Sun Nov 14 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-25.20101114hg1698
- update to latest revision 1698
- several bug fix

* Wed Oct 20 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-23.20101004hg1666
- add patch for llvm 2.8

* Fri Oct 15 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-22.20101004hg1666
- update to new release 1666

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-21.20100928hg1665
- update to new release 1665 

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-20.20100927hg1664
- update to new release 1664

* Sat Sep 18 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-19.20100905hg1659
- update to new release 1659

* Sat Sep 04 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-18.20100904hg1657
- update to new release 1657

* Thu Aug 26 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-17.20100609hg1655
- use %%{_libdir} instead %%{_libdir}/d

* Fri Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-16.20100609hg1655
- fix minor bug in /etc/ldc.conf

* Fri Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-15.20100609hg1655
- fix minor bug in /etc/ldc.conf

* Fri Aug 12 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-14.20100609hg1655
- fix critical bug in /etc/ldc.conf

* Wed Aug 11 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-13.20100609hg1655
- fix critical bug in /etc/ldc.conf

* Sun Aug 07 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-12.20100609hg1655
- Update to revision 1655

* Mon Aug 02 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-12.20100609hg1654
- Add patch

* Mon Aug 02 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-11.20100609hg1654
- Add %%{?_smp_mflags} macro for makefile
- Add flag -O2 for good optimizations in %%{_d_optflags} macro

* Sun Aug 01 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-10.20100609hg1654
- Update to revision 1654

* Fri Jul 29 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-9.20100609hg1653
- add %%{_d_libdir} macro in macros.ldc
- fix lib path in ldc.conf

* Wed Jul 28  2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-8.20100609hg1653
- Using macro for D package

* Tue Jul 27 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-7.20100609hg1653
- Fix macros.ldc name

* Tue Jul 27 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-6.20100609hg1653
- Add %%{_sysconfdir}/rpm/maco.ldc file for new macro
- Fix alphatag to YYYYMMDD instead YYYYDDMM

* Sun Jul 25 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-5.20100706hg1653
- Fix ldc.rebuild.conf file

* Fri Jul 15 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-4.20100706hg1653
- Add gcc in require

* Thu Jul 01 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-3.20100706hg1653
- Perform french description

* Sat Jun 24 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-2.20100706hg1653
- Explain why .emty file is removed

* Wed Jun 23 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-1.20100706hg1653
- Initial release
