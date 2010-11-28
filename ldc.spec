%global     alphatag        20101114
%global     hg_revision     hg1698

# The source for this package was pulled from upstream's mercurial (hg).
# Use the following commands to generate the tarball:
# hg clone -r 1698 http://bitbucket.org/lindquist/ldc ldc-20101114hg1698
# tar -cJvf ldc-20101114hg1698.tar.xz ldc-20101114hg1698

Name:           ldc
Version:        0.9.2
Release:        25.%{alphatag}%{hg_revision}%{?dist}
Summary:        A compiler for the D programming language

Group:          Development/Languages
# The DMD frontend in dmd/* GPL version 1 or artistic license
# The files gen/asmstmt.cpp and gen/asm-*.hG PL version 2+ or artistic license
License:        BSD    
URL:            http://www.dsource.org/projects/ldc
Source0:        %{name}-%{alphatag}%{hg_revision}.tar.xz
Source1:        macros.%{name}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  llvm-devel
BuildRequires:  libconfig
BuildRequires:  cmake
BuildRequires:  libconfig-devel
BuildRequires:  gc
Requires:       gcc
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

%prep
%setup -q -n %{name}-%{alphatag}%{hg_revision}
find . -type f -exec sed -i 's/\r//' {} \;
#%patch0 -p1

%build
%cmake . -DCMAKE_CXX_FLAGS:STRING=-DLLVM_REV=105825

make %{?_smp_mflags} VERBOSE=2

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/rpm
# This empty file is removed because it's never used. "lib" is explicitely used
# instead of %%_libdir because it's always used (not arch dependant)
rm %{buildroot}%{_prefix}/lib/.empty

mv %{buildroot}%{_bindir}/ldc.rebuild.conf  %{buildroot}%{_sysconfdir}/ldc.rebuild.conf
mv %{buildroot}%{_bindir}/ldc.conf          %{buildroot}%{_sysconfdir}/ldc.conf
install --mode=0644 %{SOURCE1}              %{buildroot}%{_sysconfdir}/rpm/macros.ldc

sed -i -e   "s|-I.*/../tango\"|-I /usr/include/d/tango\"|"                             \
    -e      "/^.*-I.*%{name}-%{alphatag}%{hg_revision}\/..\/tango\/user.*$/d"           \
    -e      "/^.*-I.*%{name}-%{alphatag}%{hg_revision}\/..\/tango\/lib\/common.*$/d"    \
    -e      "s|-I.*/../tango/tango/core/vendor|-I /usr/include/d/tango/core/vendor|"   \
    -e      "s|-L-L\%\%ldcbinarypath\%\%/../lib|-L-L%{_libdir}|"                      \
    -e      "s|-defaultlib=tango-user-ldc|-defaultlib=tango|"                           \
    -e      "s|-debuglib=tango-user-ldc|-debuglib=tango|"                               \
    -e      "13a \ \ \ \ \ \ \ \ \"-I /usr/include/d/\"," %{buildroot}%{_sysconfdir}/ldc.conf

sed -i "s|DFLAGS.*|DFLAGS=-I/usr/include/d -L-L %{_libdir} -d-version=Tango -defaultlib=tango -debuglib=tango|" %{buildroot}%{_sysconfdir}/ldc.rebuild.conf

chmod 755 %{buildroot}%{_bindir}/ldmd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%{_bindir}/ldc
%{_bindir}/ldmd
%config(noreplace)  %{_sysconfdir}/ldc.rebuild.conf
%config(noreplace)  %{_sysconfdir}/ldc.conf
%config(noreplace)  %{_sysconfdir}/rpm/macros.ldc

%changelog
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
