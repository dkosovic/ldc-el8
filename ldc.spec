%global     alphatag        20100706
%global     hg_revision     hg1653

# The source for this package was pulled from upstream's mercurial (hg).
# Use the following commands to generate the tarball:
# hg clone -r 1653 http://bitbucket.org/lindquist/ldc ldc-20100706hg1653
# tar -cJvf ldc-20100706hg1653.tar.xz ldc-20100706hg1653

Name:       ldc
Version:    0.9.2
Release:    1.2.%{alphatag}%{hg_revision}%{?dist}
Summary:    It is a compiler for the D programming language

Group:      Development/Languages    
License:    BSD    
URL:        http://www.dsource.org/projects/ldc
Source0:    %{name}-%{alphatag}%{hg_revision}.tar.xz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  llvm-devel
BuildRequires:  libconfig
BuildRequires:  cmake
BuildRequires:  libconfig-devel
BuildRequires:  gc
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

%build
%cmake . -DCMAKE_CXX_FLAGS:STRING=-DLLVM_REV=101676

make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir %{buildroot}/%{_sysconfdir}
# This empty file is removed because it's never used. "lib" is explicitely used
# instead of %_libdir because it's always used (not arch dependant)
rm %{buildroot}%{_prefix}/lib/.empty

mv %{buildroot}%{_bindir}/ldc.rebuild.conf  %{buildroot}%{_sysconfdir}/ldc.rebuild.conf
mv %{buildroot}%{_bindir}/ldc.conf          %{buildroot}%{_sysconfdir}/ldc.conf

sed -i "s|-I.*/../tango\"|-I%{_includedir}/d/tango\"|" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "/^.*-I.*%{name}-%{alphatag}%{hg_revision}\/..\/tango\/user.*$/d" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "/^.*-I.*%{name}-%{alphatag}%{hg_revision}\/..\/tango\/lib\/common.*$/d" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "s|-I.*/../tango/tango/core/vendor|-I%{_includedir}/d/tango/core/vendor|" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "s|-L-L\%\%ldcbinarypath\%\%/../lib|-L-L%{_libdir}/tango|" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "s|-defaultlib=tango-user-ldc|-defaultlib=tango|" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "s|-debuglib=tango-user-ldc|-debuglib=tango|" %{buildroot}%{_sysconfdir}/ldc.conf
sed -i "13a \ \ \ \ \ \ \ \ \"-I%{_includedir}/d/\"," %{buildroot}%{_sysconfdir}/ldc.conf

chmod 755 %{buildroot}%{_bindir}/ldmd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE readme.txt
%{_bindir}/ldc
%{_bindir}/ldmd
%config(noreplace) %{_sysconfdir}/ldc.rebuild.conf
%config(noreplace) %{_sysconfdir}/ldc.conf

%changelog
* Thu Jul 01 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-1.2.20100706hg1653
- Perform french description

* Sat Jun 24 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-1.1.20100706hg1653
- Explain why .emty file is removed

* Wed Jun 23 2010 Jonathan MERCIER <bioinfornatics at gmail.com> 0.9.2-1.20100706hg1653
- Initial release
