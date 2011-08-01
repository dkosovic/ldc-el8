%global     alphatag        20110901
%global     git_revision    git58d40d2

# The source for this package was pulled from upstream's subversion (svn).
# Use the following commands to generate the tarball:
# git rev-parse --short HEAD -> for get hash
# git clone git://github.com/bioinfornatics/ldc2.git ldc-20110901git58d40d2
# (cd ldc-20110901git58d40d2; git checkout 161823bef25fa366677d; git submodule init; git submodule update)
# find ldc-20110901git58d40d2 -name ".git" -print0 | xargs -0 rm -fr
# tar cJvf ldc-20110901git58d40d2.tar.xz ldc-20110901git58d40d2

Name:           ldc
Version:        2
Release:        2.%{alphatag}%{git_revision}%{?dist}
Summary:        A compiler for the D programming language

Group:          Development/Languages
# The DMD frontend in dmd/* GPL version 1 or artistic license
# The files gen/asmstmt.cpp and gen/asm-*.hG PL version 2+ or artistic license
License:        BSD    
URL:            http://www.dsource.org/projects/ldc
Source0:        %{name}-%{alphatag}%{git_revision}.tar.xz
Source1:        macros.%{name}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  llvm-devel >= 2.9
BuildRequires:  libconfig, libconfig-devel
BuildRequires:  cmake
BuildRequires:  gc, gcc-c++, gcc
Requires:       libconfig

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
Summary:        Runtime lirary for D
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

%prep
%setup -q -n %{name}-%{alphatag}%{git_revision}
find . -type f -exec sed -i 's/\r//g' {} \;
#%patch0 -p1

%build
%cmake -DD_VERSION:STRING=2 -DCONF_INST_DIR:PATH=%{_sysconfdir} -DRUNTIME_DIR=./druntime -DPHOBOS2_DIR=./phobos .

make %{?_smp_mflags} VERBOSE=2 phobos2

%install
rm -rf %{buildroot}
#make %{?_smp_mflags} install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}/%{_includedir}/d
mkdir -p %{buildroot}/%{_libdir}/
mkdir -p %{buildroot}/%{_includedir}/d/std

# This empty file is removed because it's never used. "lib" is explicitely used
# instead of %%_libdir because it's always used (not arch dependant)
#rm %{buildroot}%{_prefix}/lib/.empty

install --mode=0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.ldc

sed -i \
    -e      "10a \ \ \ \ \ \ \ \"-I%{_includedir}\/d\","        \
    -e      "/^.*-I.*%{name}-%{alphatag}%{git_revision}.*$/d"   \
    -e      "s/-L-L.*lib/-L-L$(%{_libdir})\/druntime.so/"       bin/ldc2.conf 

sed -i "s|DFLAGS.*|DFLAGS=-I%{_includedir}/d -L-L%{_libdir} -d-version=Phobos -defaultlib=phobos2 -debuglib=phobos2|" bin/ldc2.rebuild.conf

# ldc
cp -rp import/*                 %{buildroot}/%{_includedir}/d
install bin/ldc2.conf           %{buildroot}%{_sysconfdir}/ldc2.conf
install bin/ldc2.rebuild.conf   %{buildroot}%{_sysconfdir}/ldc2.rebuild.conf
install -m0755 bin/ldmd2        %{buildroot}%{_bindir}/ldmd2
install -m0755 bin/ldc2         %{buildroot}%{_bindir}/ldc2

# druntime
install lib/libdruntime-ldc.so %{buildroot}/%{_libdir}/libdruntime-ldc.so
cp -rp druntime/import/* %{buildroot}/%{_includedir}/d/

# phobos
cp -rp phobos/std %{buildroot}/%{_includedir}/d/
install lib/liblphobos2.so %{buildroot}/%{_libdir}/liblphobos2.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%{_bindir}/ldc2
%{_bindir}/ldmd2
%{_includedir}/d/core
%config(noreplace)  %{_sysconfdir}/ldc2.rebuild.conf
%config(noreplace)  %{_sysconfdir}/ldc2.conf
%config             %{_sysconfdir}/rpm/macros.ldc

%files druntime
%defattr(-,root,root,-)
%doc druntime/LICENSE_1_0.txt druntime/README.txt
%{_includedir}/d/ldc
%{_includedir}/d/object.di
%{_includedir}/d/std/intrinsic.di
%{_libdir}/libdruntime-ldc.so

%files phobos
%defattr(-,root,root,-)
%doc phobos/LICENSE_1_0.txt
%{_libdir}/liblphobos2.so
%{_includedir}/d/std

%changelog
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
