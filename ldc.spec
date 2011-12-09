# debug info seem not works with D compiler
%global     debug_package %{nil}
%global     snapdate        20111206
%global     ldc_rev         fa5fb92
%global     phobos_rev      2bebc8f
%global     druntime_rev    24e79c6
%global     alphatag        %{snapdate}git%{ldc_rev}
%global     phobostag       %{snapdate}git%{phobos_rev}
%global     druntimetag     %{snapdate}git%{druntime_rev}

# The source for this package was pulled from upstream's git.
# Use the following commands to generate the tarball:
# cd ldc; git rev-parse --short HEAD            -> for ldc_rev
# cd ldc/phobos; git rev-parse --short HEAD     -> for phobos_rev
# cd ldc/druntime/;  git rev-parse --short HEAD -> for druntime_rev
# git clone https://github.com/ldc-developers/ldc.git
# cd ldc; git submodule update -i; git checkout %%ldc_rev  
# git archive --prefix=ldc-%%{alphatag}/ HEAD | xz > ../ldc-%%{alphatag}.xz
# cd runtime/druntime
# git archive --prefix=runtime/druntime/ HEAD | xz > ../../../ldc-druntime-%%{druntimetag}.xz
# cd ../phobos
# git archive --prefix=runtime/phobos/ HEAD | xz > ../../../ldc-phobos-%%{phobostag}.xz

Name:           ldc
Version:        2
Release:        9.%{alphatag}%{?dist}
Summary:        A compiler for the D programming language

Group:          Development/Languages
# The DMD frontend in dmd/* GPL version 1 or artistic license
# The files gen/asmstmt.cpp and gen/asm-*.hG PL version 2+ or artistic license
License:        BSD    
URL:            http://www.dsource.org/projects/ldc
Source0:        %{name}-%{alphatag}.xz
Source1:        %{name}-phobos-%{phobostag}.xz
Source2:        %{name}-druntime-%{druntimetag}.xz
Source3:        macros.%{name}
Source4:        DdocToDevhelp
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  llvm-devel >= 3.0
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
Requires:       %{name}-druntime


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
Requires:       %{name}-phobos
Requires:       %{name}-druntime-devel

%description phobos-devel
The phobos-devel package contains header files for developing D
applications that use phobos.

%description phobos-devel -l fr
Le paquet phobos-devel contient les fichiers d'entêtes pour développer
des applications en D utilisant phobos.

%package phobos-geany-tags
Summary:        Support for enable autocompletion in geany
Group:          Development/Tools
Requires:       %{name} =  %{version}-%{release}
BuildRequires:  geany
Requires:       geany

%description phobos-geany-tags
Enable autocompletion for phobos library in geany (IDE)

%description -l fr phobos-geany-tags
Active l'autocompletion pour pour la bibliothèque phobos dans geany (IDE)

%package phobos-devhelp
Summary:        Phobos user and reference manuals
Group:          Development/Tools
Requires:       %{name} =  %{version}-%{release}
BuildRequires:  python
Requires:       devhelp

%description phobos-devhelp
User Manual and Reference, Manual are provided in HTML format. You can use
devhelp to browse it.

%description -l fr phobos-devhelp
Manuel et référence, le manuel est fournit au format HTML. Vous pouez utilisez
devhelp pour le parcourir

%prep
%setup -q -n %{name}-%{alphatag}
%setup -q -T -D -a 1 -n %{name}-%{alphatag}
%setup -q -T -D -a 2 -n %{name}-%{alphatag}
find . -type f -exec sed -i 's/\r//g' {} \;
# temp geany config directory for allow geany to generate tags
mkdir geany_config
# fix install
# sed -i "81a \ \ \ \ file(COPY \${RUNTIME_DIR}/src/core/bitop.d DESTINATION \${PROJECT_BINARY_DIR}/import/core/ )" runtime/CMakeLists.txt

%build
%cmake  -DMULTILIB:BOOL=OFF -DBUILD_SHARED_LIBS:BOOL=ON  -DINCLUDE_INSTALL_DIR:PATH=%{_includedir}/d .
make %{?_smp_mflags} VERBOSE=2 phobos2

# generate geany tags
geany -c geany_config -g phobos.d.tags $(find runtime/phobos/std -name "*.d")

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/rpm
mkdir -p %{buildroot}/%{_includedir}/d/ldc
mkdir -p %{buildroot}/%{_datadir}/geany/tags/
mkdir -p %{buildroot}/%{_datadir}/devhelp/books/Phobos
# macros for D package
install --mode=0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.ldc
# geany tags
install -m0755 phobos.d.tags %{buildroot}/%{_datadir}/geany/tags/
%{SOURCE4} -n Phobos -s %{buildroot}/%{_includedir}/d/std/ -p %{buildroot}/%{_datadir}

%clean
rm -rf %{buildroot}

%post               -p  /sbin/ldconfig
%postun             -p  /sbin/ldconfig
%post   druntime    -p  /sbin/ldconfig
%postun druntime    -p  /sbin/ldconfig
%post   phobos      -p  /sbin/ldconfig
%postun phobos      -p  /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%config(noreplace)  %{_sysconfdir}/ldc2.rebuild.conf
%config(noreplace)  %{_sysconfdir}/ldc2.conf
%config             %{_sysconfdir}/rpm/macros.ldc
%{_sysconfdir}/bash_completion.d/ldc
%{_bindir}/ldc2
%{_bindir}/ldmd2

%files druntime
%defattr(-,root,root,-)
%doc runtime/druntime/LICENSE_1_0.txt runtime/druntime/README.txt
%{_libdir}/libdruntime-ldc.so

%files druntime-devel
%defattr(-,root,root,-)
%{_includedir}/d/ldc
%{_includedir}/d/core

%files phobos
%defattr(-,root,root,-)
%doc runtime/phobos/LICENSE_1_0.txt
%{_libdir}/libphobos2-ldc.so

%files phobos-devel
%defattr(-,root,root,-)
%{_includedir}/d/crc32.d
%{_includedir}/d/std
%{_includedir}/d/etc

%files phobos-geany-tags
%defattr(-,root,root,-)
%{_datadir}/geany/tags/phobos.d.tags

%files phobos-devhelp
%defattr(-,root,root,-)
%{_datadir}/devhelp/books/Phobos

%changelog
* Fri Dec 9 2011  Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-9.20111206gitfa5fb92
- Add doc for devhelp

* Wed Dec 6 2011  Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-8.20111206gitfa5fb92
- Put %%{_d_includedir}/core into druntime-devel package

* Wed Dec 6 2011  Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-8.20111206git641cc85
- Update compiler to latest revision
- Update runtime to latest revision
- Update phobos to latest revision

* Thu Dec 1 2011  Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-7.20111117git4add11b
- Update to latest revision
- fix dependencies

* Sat Nov 9 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-6.20111112gitd9da872
- Update to latest revision

* Thu Nov 9 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-5.20110911git3cf958ad
- Update to latest revision

* Sat Sep 17 2011 Jonathan MERCIER <bioinfornatics@fedoraproject.org> - 2-4.20110915git423076d
- Update to latest revision

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
