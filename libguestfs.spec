#
# TODO: php, ruby and haskell bindings
#
# Conditional build:
%bcond_with	static_libs	# build static libraries
#
%include	/usr/lib/rpm/macros.perl
%include	/usr/lib/rpm/macros.java
Summary:	Tools for accessing and modifying virtual machine disk images
Summary(pl.UTF-8):	Narzędzia do dostępu i modyfikacji obrazów dysków maszyn wirtualnych
Name:		libguestfs
Version:	1.12.7
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://libguestfs.org/download/1.12-stable/%{name}-%{version}.tar.gz
# Source0-md5:	b8099728e7516bbb9c7e3df96f3c7f30
Patch0:		ncurses.patch
URL:		http://libguestfs.org/
BuildRequires:	attr-devel
BuildRequires:	augeas-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cdrkit-mkisofs
BuildRequires:	db-utils
#BuildRequires:	febootstrap
BuildRequires:	gettext-devel
BuildRequires:	gperf
BuildRequires:	hivex-devel
BuildRequires:	jdk
BuildRequires:	libconfig-devel
BuildRequires:	libmagic-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	libvirt-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxml2-progs
BuildRequires:	ncurses-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-pcre-devel
BuildRequires:	pcre-devel
BuildRequires:	perl
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(Locale::TextDomain)
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(String::ShellQuote)
BuildRequires:	perl(Sys::Virt)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Win::Hivex)
BuildRequires:	perl(Win::Hivex::Regedit)
BuildRequires:	perl-tools-pod
#BuildRequires:	php-devel
BuildRequires:	po4a
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	readline-devel
#BuildRequires:	ruby
#BuildRequires:	ruby-devel
Requires:	qemu
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libguestfs is a set of tools for accessing and modifying virtual
machine (VM) disk images. You can use this for viewing and editing
files inside guests, scripting changes to VMs, monitoring disk
used/free statistics, P2V, V2V, performing partial backups, cloning
VMs, and much else besides.

%package devel
Summary:	Header files for libguestfs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libguestfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libguestfs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libguestfs.

%package static
Summary:	Static libguestfs library
Summary(pl.UTF-8):	Statyczna biblioteka libguestfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libguestfs library.

%description static -l pl.UTF-8
Statyczna biblioteka libguestfs.

%package -n perl-libguestfs
Summary:	Perl bindings for libguestfs
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}


%description -n perl-libguestfs
Perl bindings for libguestfs.

%package -n java-libguestfs
Summary:	Java bindings for libguestfs
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-libguestfs
Java bindings for libguestfs.

%package -n java-libguestfs-javadoc
Summary:	Java bindings for libguestfs - documentation
Group:		Documentation

%description -n java-libguestfs-javadoc
Java bindings for libguestfs - documentation.

%package -n ocaml-libguestfs
Summary:	OCaml bindings for libguestfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-libguestfs
OCaml bindings for libguestfs.

%package -n ocaml-libguestfs-devel
Summary:	Header files for ocaml-libguestfs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ocaml-libguestfs
Group:		Development/Libraries
Requires:	ocaml-%{name} = %{version}-%{release}

%description -n ocaml-libguestfs-devel
Header files for ocaml-libguestfs library.

%description -n ocaml-libguestfs-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ocaml-libguestfs.

%package -n python-libguestfs
Summary:	Python bindings for libguestfs
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libguestfs
Python bindings for libguestfs.

%package -n bash-completion-libguestfs
Summary:	bash-completion for libguestfs tools
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-libguestfs
bash-completion for guestfish tool.

%prep
%setup -q
%patch0 -p1

%build
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure \
	vmchannel_test=no \
	QEMU=/usr/bin/qemu \
	--with-java-home=%{java_home} \
	--with-qemu=qemu \
	--disable-haskell \
	--disable-ruby \
	--disable-appliance \
	%{__enable_disable static_libs static} \
	--disable-silent-rules

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{py_sitedir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README RELEASE-NOTES ROADMAP TODO
%attr(755,root,root) %{_bindir}/guestfish
%attr(755,root,root) %{_bindir}/guestmount
%attr(755,root,root) %{_bindir}/libguestfs-test-tool
%attr(755,root,root) %{_bindir}/virt-cat
%attr(755,root,root) %{_bindir}/virt-copy-in
%attr(755,root,root) %{_bindir}/virt-copy-out
%attr(755,root,root) %{_bindir}/virt-df
%attr(755,root,root) %{_bindir}/virt-edit
%attr(755,root,root) %{_bindir}/virt-filesystems
%attr(755,root,root) %{_bindir}/virt-inspector
%attr(755,root,root) %{_bindir}/virt-list-filesystems
%attr(755,root,root) %{_bindir}/virt-list-partitions
%attr(755,root,root) %{_bindir}/virt-ls
%attr(755,root,root) %{_bindir}/virt-make-fs
%attr(755,root,root) %{_bindir}/virt-rescue
%attr(755,root,root) %{_bindir}/virt-resize
%attr(755,root,root) %{_bindir}/virt-tar
%attr(755,root,root) %{_bindir}/virt-tar-in
%attr(755,root,root) %{_bindir}/virt-tar-out
%attr(755,root,root) %{_bindir}/virt-win-reg
%attr(755,root,root) %{_libdir}/libguestfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguestfs.so.0
/etc/libguestfs-tools.conf
%{_mandir}/man1/guestfish.1*
%{_mandir}/man1/guestfs-recipes.1*
%{_mandir}/man1/guestmount.1*
%{_mandir}/man1/libguestfs-test-tool.1*
%{_mandir}/man1/virt-cat.1*
%{_mandir}/man1/virt-copy-in.1*
%{_mandir}/man1/virt-copy-out.1*
%{_mandir}/man1/virt-df.1*
%{_mandir}/man1/virt-edit.1*
%{_mandir}/man1/virt-filesystems.1*
%{_mandir}/man1/virt-inspector.1*
%{_mandir}/man1/virt-list-filesystems.1*
%{_mandir}/man1/virt-list-partitions.1*
%{_mandir}/man1/virt-ls.1*
%{_mandir}/man1/virt-make-fs.1*
%{_mandir}/man1/virt-rescue.1*
%{_mandir}/man1/virt-resize.1*
%{_mandir}/man1/virt-tar-in.1*
%{_mandir}/man1/virt-tar-out.1*
%{_mandir}/man1/virt-tar.1*
%{_mandir}/man1/virt-win-reg.1*
%lang(ja) %{_mandir}/ja/man1/guestfish.1*
%lang(ja) %{_mandir}/ja/man1/guestmount.1*
%lang(ja) %{_mandir}/ja/man1/virt-cat.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-out.1*
%lang(ja) %{_mandir}/ja/man1/virt-df.1*
%lang(ja) %{_mandir}/ja/man1/virt-edit.1*
%lang(ja) %{_mandir}/ja/man1/virt-filesystems.1*
%lang(ja) %{_mandir}/ja/man1/virt-inspector.1*
%lang(ja) %{_mandir}/ja/man1/virt-list-filesystems.1*
%lang(ja) %{_mandir}/ja/man1/virt-list-partitions.1*
%lang(ja) %{_mandir}/ja/man1/virt-ls.1*
%lang(ja) %{_mandir}/ja/man1/virt-make-fs.1*
%lang(ja) %{_mandir}/ja/man1/virt-rescue.1*
%lang(ja) %{_mandir}/ja/man1/virt-resize.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-out.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar.1*
%lang(ja) %{_mandir}/ja/man1/virt-win-reg.1*
%lang(uk) %{_mandir}/uk/man1/guestfish.1*
%lang(uk) %{_mandir}/uk/man1/guestmount.1*
%lang(uk) %{_mandir}/uk/man1/virt-cat.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-out.1*
%lang(uk) %{_mandir}/uk/man1/virt-df.1*
%lang(uk) %{_mandir}/uk/man1/virt-edit.1*
%lang(uk) %{_mandir}/uk/man1/virt-filesystems.1*
%lang(uk) %{_mandir}/uk/man1/virt-inspector.1*
%lang(uk) %{_mandir}/uk/man1/virt-list-filesystems.1*
%lang(uk) %{_mandir}/uk/man1/virt-list-partitions.1*
%lang(uk) %{_mandir}/uk/man1/virt-ls.1*
%lang(uk) %{_mandir}/uk/man1/virt-make-fs.1*
%lang(uk) %{_mandir}/uk/man1/virt-rescue.1*
%lang(uk) %{_mandir}/uk/man1/virt-resize.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-out.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar.1*
%lang(uk) %{_mandir}/uk/man1/virt-win-reg.1*

%files devel
%defattr(644,root,root,755)
#%doc devel-doc/*
%{_libdir}/libguestfs.so
%{_includedir}/guestfs.h
%{_pkgconfigdir}/libguestfs.pc
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/libguestfs.3*
%{_mandir}/ja/man3/guestfs.3*
%{_mandir}/uk/man3/guestfs.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libguestfs.a
%endif

%files -n perl-libguestfs
%defattr(644,root,root,755)
%{perl_vendorarch}/Sys/Guestfs.pm
%{perl_vendorarch}/Sys/Guestfs/Lib.pm
%{perl_vendorarch}/Sys/bindtests.pl
%{perl_vendorarch}/auto/Sys/Guestfs/.packlist
%{perl_vendorarch}/auto/Sys/Guestfs/Guestfs.bs
%{perl_vendorarch}/auto/Sys/Guestfs/Guestfs.so
%{_mandir}/man3/guestfs-perl.3*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/Sys::Guestfs::Lib.3pm*

%files -n java-libguestfs
%defattr(644,root,root,755)
%{_libdir}/libguestfs_jni.so
%{_libdir}/libguestfs_jni.so.1
%{_libdir}/libguestfs_jni.so.1.12.7
%{_datadir}/java/libguestfs-1.12.7.jar
%{_mandir}/man3/guestfs-java.3*

%files -n java-libguestfs-javadoc
%defattr(644,root,root,755)
%{_javadocdir}/libguestfs-java-1.12.7

%files -n ocaml-libguestfs
%defattr(644,root,root,755)
%{_libdir}/ocaml/stublibs/dllmlguestfs.so
%{_libdir}/ocaml/stublibs/dllmlguestfs.so.owner
%{_mandir}/man3/guestfs-ocaml.3*

%files -n ocaml-libguestfs-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/guestfs/META
%{_libdir}/ocaml/guestfs/bindtests.cmi
%{_libdir}/ocaml/guestfs/bindtests.cmx
%{_libdir}/ocaml/guestfs/guestfs.cmi
%{_libdir}/ocaml/guestfs/guestfs.cmx
%{_libdir}/ocaml/guestfs/guestfs.mli
%{_libdir}/ocaml/guestfs/libmlguestfs.a
%{_libdir}/ocaml/guestfs/mlguestfs.a
%{_libdir}/ocaml/guestfs/mlguestfs.cma
%{_libdir}/ocaml/guestfs/mlguestfs.cmxa

%files -n python-libguestfs
%defattr(644,root,root,755)
%{_mandir}/man3/guestfs-python.3*
%{py_sitedir}/guestfs.py
%{py_sitedir}/libguestfsmod.so

%files -n bash-completion-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) /etc/bash_completion.d/guestfish-bash-completion.sh
