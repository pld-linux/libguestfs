# TODO:
# - finish haskell bindings (when finished upstream, not ready as of 1.20.2)
# - systemtap probes
# - PLD appliance support? (needs at least package list adjustment)
#
# Conditional build:
%bcond_with	static_libs	# build static libraries
%bcond_without	erlang		# Erlang binding
%bcond_with	haskell		# Haskell (GHC) binding [incomplete, nothing is installed]
%bcond_without	java		# Java binding
%bcond_without	lua		# Lua binding
%bcond_without	ocaml		# OCaml binding and tools
%bcond_without	perl		# Perl binding
%bcond_without	perltools	# Perl tools
%bcond_without	php		# PHP binding
%bcond_without	python		# Python binding
%bcond_without	ruby		# Ruby binding
#

%include	/usr/lib/rpm/macros.perl
%include	/usr/lib/rpm/macros.java
Summary:	Library and tools for accessing and modifying virtual machine disk images
Summary(pl.UTF-8):	Biblioteka i narzędzia do dostępu i modyfikacji obrazów dysków maszyn wirtualnych
Name:		libguestfs
Version:	1.20.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://libguestfs.org/download/1.20-stable/%{name}-%{version}.tar.gz
# Source0-md5:	a5717d7d3975a141c553dd8a8633d5dd
Patch0:		ncurses.patch
Patch1:		augeas-libxml2.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-am.patch
URL:		http://libguestfs.org/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	augeas-devel >= 0.5.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cdrkit-mkisofs
BuildRequires:	cpio
BuildRequires:	db-utils
# erl_interface package
%{?with_erlang:BuildRequires:	erlang}
#BuildRequires:	febootstrap >= 3.20
BuildRequires:	gettext-devel
%{?with_haskell:BuildRequires:	ghc}
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gperf
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	hivex-devel >= 1.2.7
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libcap-devel
BuildRequires:	libconfig-devel
BuildRequires:	libfuse-devel
BuildRequires:	libmagic-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	libvirt-devel >= 0.10.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxml2-progs
%if %{with lua}
# use 5.2 as 5.1 packaging in PLD was incompatible with what's expected by configure
BuildRequires:	lua52
BuildRequires:	lua52-devel
%endif
BuildRequires:	ncurses-devel
%if %{with ocaml}
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-gettext-devel
BuildRequires:	ocaml-pcre-devel
%endif
BuildRequires:	pcre-devel
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
%if %{with perl}
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Test-Simple
%endif
%if %{with perltools}
BuildRequires:	perl-String-ShellQuote
BuildRequires:	perl-Sys-Virt
BuildRequires:	perl-hivex >= 1.2.7
BuildRequires:	perl-libintl
BuildRequires:	perl-modules
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(Locale::TextDomain)
BuildRequires:	perl(Pod::Man)
BuildRequires:	perl(Pod::Simple)
BuildRequires:	perl(Pod::Usage)
%endif
%{?with_php:BuildRequires:	php-devel}
BuildRequires:	pkgconfig
BuildRequires:	po4a
%if %{with python}
BuildRequires:	python
BuildRequires:	python-devel
%endif
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.322
%if %{with ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-rake
%endif
BuildRequires:	yajl-devel >= 2
Requires:	qemu-common >= 1.1.0
Suggests:	db-utils
Suggests:	icoutils
Suggests:	netpbm-progs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libguestfs is a library and set of tools for accessing and modifying
virtual machine (VM) disk images. You can use this for viewing and
editing files inside guests, scripting changes to VMs, monitoring disk
used/free statistics, P2V, V2V, performing partial backups, cloning
VMs, and much else besides.

%description -l pl.UTF-8
libguestfs to biblioteka oraz zestaw narzędzi do dostępu oraz
modyfikowania obrazów dysków maszyn wirtualnych (VM). Można je
wykorzystywać do oglądania i edycji plików wewnątrz gości, zmian
skryptowych w VM-ach, monitorowania statystyk używanego/dostępnego
miejsca na dyskach, P2V, V2V, wykonywania częściowych kopii
zapasowych, klonowania VM-ów i wielu podobnych operacji.

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

%package apidocs
Summary:	libguestfs API documentation
Summary(pl.UTF-8):	Dokumentacja API libguestfs
Group:		Documentation

%description apidocs
libguestfs API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libguestfs.

%package gobject
Summary:	GObject bindings to libguestfs library
Summary(pl.UTF-8):	Wiązania GObject do biblioteki libguestfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0

%description gobject
GObject bindings to libguestfs library.

%description gobject -l pl.UTF-8
Wiązania GObject do biblioteki libguestfs.

%package gobject-devel
Summary:	Header files for libguestfs-gobject library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libguestfs-gobject
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gobject = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0

%description gobject-devel
Header files for libguestfs-gobject library.

%description gobject-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libguestfs-gobject.

%package gobject-static
Summary:	Static libguestfs-gobject library
Summary(pl.UTF-8):	Statyczna biblioteka libguestfs-gobject
Group:		Development/Libraries
Requires:	%{name}-gobject-devel = %{version}-%{release}

%description gobject-static
Static libguestfs-gobject library.

%description gobject-static -l pl.UTF-8
Statyczna biblioteka libguestfs-gobject.

%package tools
Summary:	libguestfs tools for accessing and modifying virtual machine disk images
Summary(pl.UTF-8):	Narzędzia libguestfs do dostępu i modyfikacji obrazów dysków maszyn wirtualnych
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
%{?with_ocaml:Requires:	ocaml-libguestfs = %{version}-%{release}}
%{?with_perltools:Requires:	perl-libguestfs = %{version}-%{release}}

%description tools
libguestfs tools for accessing and modifying virtual machine (VM) disk
images. You can use this for viewing and editing files inside guests,
scripting changes to VMs, monitoring disk used/free statistics, P2V,
V2V, performing partial backups, cloning VMs, and much else besides.

%description tools -l pl.UTF-8
Zestaw narzędzi libguestfs do dostępu oraz modyfikowania obrazów
dysków maszyn wirtualnych (VM). Można je wykorzystywać do oglądania i
edycji plików wewnątrz gości, zmian skryptowych w VM-ach,
monitorowania statystyk używanego/dostępnego miejsca na dyskach, P2V,
V2V, wykonywania częściowych kopii zapasowych, klonowania VM-ów i
wielu podobnych operacji.

%package -n erlang-libguestfs
Summary:	Erlang bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Erlanga do libguestfs
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n erlang-libguestfs
Erlang bindings for libguestfs.

%description -n erlang-libguestfs -l pl.UTF-8
Wiązania Erlanga do libguestfs.

%package -n java-libguestfs
Summary:	Java bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Javy do libguestfs
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-libguestfs
Java bindings for libguestfs.

%description -n java-libguestfs -l pl.UTF-8
Wiązania Javy do libguestfs.

%package -n java-libguestfs-javadoc
Summary:	Java bindings for libguestfs - documentation
Summary(pl.UTF-8):	Wiązania Javy do libguestfs - dokumentacja
Group:		Documentation

%description -n java-libguestfs-javadoc
Java bindings for libguestfs - documentation.

%description -n java-libguestfs-javadoc -l pl.UTF-8
Wiązania Javy do libguestfs - dokumentacja.

%package -n lua-libguestfs
Summary:	Lua bindings for libguestfs
Summary(pl.UTF-8):	Wiązania języka Lua do libguestfs
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n lua-libguestfs
Lua bindings for libguestfs.

%description -n lua-libguestfs -l pl.UTF-8
Wiązania języka Lua do libguestfs.

%package -n ocaml-libguestfs
Summary:	OCaml bindings for libguestfs
Summary(pl.UTF-8):	Wiązania OCamla do libguestfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ocaml-libguestfs
OCaml bindings for libguestfs.

%description -n ocaml-libguestfs -l pl.UTF-8
Wiązania OCamla do libguestfs.

%package -n ocaml-libguestfs-devel
Summary:	Development files OCaml libguestfs bindings
Summary(pl.UTF-8):	Pliki programistyczne wiązań OCamla do libguestfs
Group:		Development/Libraries
Requires:	ocaml-%{name} = %{version}-%{release}

%description -n ocaml-libguestfs-devel
Development files OCaml libguestfs bindings.

%description -n ocaml-libguestfs-devel -l pl.UTF-8
Pliki programistyczne wiązań OCamla do libguestfs.

%package -n perl-libguestfs
Summary:	Perl bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Perla do libguestfs
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Suggests:	perl-Sys-Virt
Suggests:	perl-XML-XPath
Suggests:	perl-hivex >= 1.2.7

%description -n perl-libguestfs
Perl bindings for libguestfs.

%description -n perl-libguestfs -l pl.UTF-8
Wiązania Perla do libguestfs.

%package -n php-guestfs
Summary:	PHP bindings for libguestfs
Summary(pl.UTF-8):	Wiązania PHP do libguestfs
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n php-guestfs
PHP bindings for libguestfs.

%description -n php-guestfs -l pl.UTF-8
Wiązania PHP do libguestfs.

%package -n python-libguestfs
Summary:	Python bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Pythona do libguestfs
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libguestfs
Python bindings for libguestfs.

%description -n python-libguestfs -l pl.UTF-8
Wiązania Pythona do libguestfs.

%package -n ruby-libguestfs
Summary:	Ruby bindings for libguestfs
Summary(pl.UTF-8):	Wiązania języka Ruby do libguestfs
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
%{?ruby_ver_requires_eq}

%description -n ruby-libguestfs
Ruby bindings for libguestfs.

%description -n ruby-libguestfs -l pl.UTF-8
Wiązania języka Ruby do libguestfs.

%package -n bash-completion-libguestfs
Summary:	bash-completion for libguestfs tools
Summary(pl.UTF-8):	Bashowe uzupełnianie argumentów dla narzędzi libguestfs
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-libguestfs
bash-completion for guestfish tool.

%description -n bash-completion-libguestfs -l pl.UTF-8
Bashowe uzupełnianie argumentów dla narzędzi libguestfs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	vmchannel_test=no \
	%{?with_lua:LUA=/usr/bin/lua5.2} \
	PBMTEXT=/usr/bin/pbmtext \
	PNMTOPNG=/usr/bin/pnmtopng \
	BMPTOPNM=/usr/bin/bmptopnm \
	PAMCUT=/usr/bin/pamcut \
	WRESTOOL=/usr/bin/wrestool \
	QEMU=%{_bindir}/qemu \
	--with-html-dir=%{_gtkdocdir} \
	--with-java=%{?with_java:%{java_home}}%{!?with_java:no} \
	--with-qemu=qemu \
	--enable-install-daemon \
	--disable-appliance \
	%{!?with_erlang:--disable-erlang} \
	%{!?with_haskell:--disable-haskell} \
	%{!?with_lua:--disable-lua} \
	%{!?with_ocaml:--disable-ocaml} \
	%{!?with_perl:--disable-perl} \
	%{!?with_php:--disable-php} \
	%{!?with_python:--disable-python} \
	%{!?with_ruby:--disable-ruby} \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT \
	phpdir=%{_sysconfdir}/php/conf.d

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%if %{with lua}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lua/*/*.la
%endif
%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%endif

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	gobject -p /sbin/ldconfig
%postun	gobject -p /sbin/ldconfig

%post	-n java-libguestfs -p /sbin/ldconfig
%postun	-n java-libguestfs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README ROADMAP TODO
%attr(755,root,root) %{_libdir}/libguestfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguestfs.so.0
%{_mandir}/man1/guestfs-release-notes.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-release-notes.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-release-notes.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguestfs.so
%{_includedir}/guestfs.h
%{_pkgconfigdir}/libguestfs.pc
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/libguestfs.3*
%lang(ja) %{_mandir}/ja/man3/guestfs.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-examples.3*
%lang(uk) %{_mandir}/uk/man3/guestfs.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-examples.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libguestfs.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/guestfs

%files gobject
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguestfs-gobject-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguestfs-gobject-1.0.so.0
%{_libdir}/girepository-1.0/Guestfs-1.0.typelib

%files gobject-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguestfs-gobject-1.0.so
%{_includedir}/guestfs-gobject.h
%{_includedir}/guestfs-gobject
%{_datadir}/gir-1.0/Guestfs-1.0.gir
%{_pkgconfigdir}/libguestfs-gobject-1.0.pc

%if %{with static_libs}
%files gobject-static
%defattr(644,root,root,755)
%{_libdir}/libguestfs-gobject-1.0.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/guestfish
%attr(755,root,root) %{_bindir}/guestmount
%attr(755,root,root) %{_bindir}/libguestfs-test-tool
%attr(755,root,root) %{_bindir}/virt-alignment-scan
%attr(755,root,root) %{_bindir}/virt-cat
%attr(755,root,root) %{_bindir}/virt-copy-in
%attr(755,root,root) %{_bindir}/virt-copy-out
%attr(755,root,root) %{_bindir}/virt-df
%attr(755,root,root) %{_bindir}/virt-edit
%attr(755,root,root) %{_bindir}/virt-filesystems
%attr(755,root,root) %{_bindir}/virt-format
%attr(755,root,root) %{_bindir}/virt-inspector
%attr(755,root,root) %{_bindir}/virt-ls
%attr(755,root,root) %{_bindir}/virt-rescue
%attr(755,root,root) %{_bindir}/virt-tar-in
%attr(755,root,root) %{_bindir}/virt-tar-out
%attr(755,root,root) %{_sbindir}/guestfsd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libguestfs-tools.conf
%{_mandir}/man1/guestfish.1*
%{_mandir}/man1/guestfs-faq.1*
%{_mandir}/man1/guestfs-performance.1*
%{_mandir}/man1/guestfs-recipes.1*
%{_mandir}/man1/guestfs-testing.1*
%{_mandir}/man1/guestmount.1*
%{_mandir}/man1/libguestfs-test-tool.1*
%{_mandir}/man1/virt-alignment-scan.1*
%{_mandir}/man1/virt-cat.1*
%{_mandir}/man1/virt-copy-in.1*
%{_mandir}/man1/virt-copy-out.1*
%{_mandir}/man1/virt-df.1*
%{_mandir}/man1/virt-edit.1*
%{_mandir}/man1/virt-filesystems.1*
%{_mandir}/man1/virt-format.1*
%{_mandir}/man1/virt-inspector.1*
%{_mandir}/man1/virt-ls.1*
%{_mandir}/man1/virt-rescue.1*
%{_mandir}/man1/virt-tar-in.1*
%{_mandir}/man1/virt-tar-out.1*
%{_mandir}/man8/guestfsd.8*
%lang(ja) %{_mandir}/ja/man1/guestfish.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-faq.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-performance.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-recipes.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-testing.1*
%lang(ja) %{_mandir}/ja/man1/guestmount.1*
#%lang(ja) %{_mandir}/ja/man1/libguestfs-make-fixed-appliance.1*
%lang(ja) %{_mandir}/ja/man1/libguestfs-test-tool.1*
%lang(ja) %{_mandir}/ja/man1/virt-alignment-scan.1*
%lang(ja) %{_mandir}/ja/man1/virt-cat.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-out.1*
%lang(ja) %{_mandir}/ja/man1/virt-df.1*
%lang(ja) %{_mandir}/ja/man1/virt-edit.1*
%lang(ja) %{_mandir}/ja/man1/virt-filesystems.1*
%lang(ja) %{_mandir}/ja/man1/virt-format.1*
%lang(ja) %{_mandir}/ja/man1/virt-inspector.1*
%lang(ja) %{_mandir}/ja/man1/virt-ls.1*
%lang(ja) %{_mandir}/ja/man1/virt-rescue.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-out.1*
%lang(uk) %{_mandir}/uk/man1/guestfish.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-faq.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-performance.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-recipes.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-testing.1*
%lang(uk) %{_mandir}/uk/man1/guestmount.1*
#%lang(uk) %{_mandir}/uk/man1/libguestfs-make-fixed-appliance.1*
%lang(uk) %{_mandir}/uk/man1/libguestfs-test-tool.1*
%lang(uk) %{_mandir}/uk/man1/virt-alignment-scan.1*
%lang(uk) %{_mandir}/uk/man1/virt-cat.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-out.1*
%lang(uk) %{_mandir}/uk/man1/virt-df.1*
%lang(uk) %{_mandir}/uk/man1/virt-edit.1*
%lang(uk) %{_mandir}/uk/man1/virt-filesystems.1*
%lang(uk) %{_mandir}/uk/man1/virt-format.1*
%lang(uk) %{_mandir}/uk/man1/virt-inspector.1*
%lang(uk) %{_mandir}/uk/man1/virt-ls.1*
%lang(uk) %{_mandir}/uk/man1/virt-rescue.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-out.1*
%if %{with ocaml}
%attr(755,root,root) %{_bindir}/virt-resize
%attr(755,root,root) %{_bindir}/virt-sparsify
%attr(755,root,root) %{_bindir}/virt-sysprep
%{_mandir}/man1/virt-resize.1*
%{_mandir}/man1/virt-sparsify.1*
%{_mandir}/man1/virt-sysprep.1*
%lang(ja) %{_mandir}/ja/man1/virt-resize.1*
%lang(ja) %{_mandir}/ja/man1/virt-sparsify.1*
%lang(ja) %{_mandir}/ja/man1/virt-sysprep.1*
%lang(uk) %{_mandir}/uk/man1/virt-resize.1*
%lang(uk) %{_mandir}/uk/man1/virt-sparsify.1*
%lang(uk) %{_mandir}/uk/man1/virt-sysprep.1*
%endif
%if %{with perltools}
%attr(755,root,root) %{_bindir}/virt-list-filesystems
%attr(755,root,root) %{_bindir}/virt-list-partitions
%attr(755,root,root) %{_bindir}/virt-make-fs
%attr(755,root,root) %{_bindir}/virt-tar
%attr(755,root,root) %{_bindir}/virt-win-reg
%{_mandir}/man1/virt-list-filesystems.1*
%{_mandir}/man1/virt-list-partitions.1*
%{_mandir}/man1/virt-make-fs.1*
%{_mandir}/man1/virt-tar.1*
%{_mandir}/man1/virt-win-reg.1*
%lang(ja) %{_mandir}/ja/man1/virt-list-filesystems.1*
%lang(ja) %{_mandir}/ja/man1/virt-list-partitions.1*
%lang(ja) %{_mandir}/ja/man1/virt-make-fs.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar.1*
%lang(ja) %{_mandir}/ja/man1/virt-win-reg.1*
%lang(uk) %{_mandir}/uk/man1/virt-list-filesystems.1*
%lang(uk) %{_mandir}/uk/man1/virt-list-partitions.1*
%lang(uk) %{_mandir}/uk/man1/virt-make-fs.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar.1*
%lang(uk) %{_mandir}/uk/man1/virt-win-reg.1*
%endif

%if %{with erlang}
%files -n erlang-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erl-guestfs
%{_libdir}/erlang/lib/libguestfs-%{version}
%{_mandir}/man3/guestfs-erlang.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-erlang.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-erlang.3*
%endif

%if %{with java}
%files -n java-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguestfs_jni.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguestfs_jni.so.1
%attr(755,root,root) %{_libdir}/libguestfs_jni.so
%{_javadir}/libguestfs-%{version}.jar
%{_mandir}/man3/guestfs-java.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-java.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-java.3*

%files -n java-libguestfs-javadoc
%defattr(644,root,root,755)
%{_javadocdir}/libguestfs-java-%{version}
%endif

%if %{with lua}
%files -n lua-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lua/*/guestfs.so
%{_mandir}/man3/guestfs-lua.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-lua.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-lua.3*
%endif

%if %{with ocaml}
%files -n ocaml-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlguestfs.so
%{_libdir}/ocaml/stublibs/dllmlguestfs.so.owner

%files -n ocaml-libguestfs-devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/guestfs
%{_libdir}/ocaml/guestfs/META
%{_libdir}/ocaml/guestfs/guestfs.cmi
%{_libdir}/ocaml/guestfs/guestfs.cmx
%{_libdir}/ocaml/guestfs/guestfs.mli
%{_libdir}/ocaml/guestfs/libmlguestfs.a
%{_libdir}/ocaml/guestfs/mlguestfs.a
%{_libdir}/ocaml/guestfs/mlguestfs.cma
%{_libdir}/ocaml/guestfs/mlguestfs.cmxa
%{_mandir}/man3/guestfs-ocaml.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-ocaml.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-ocaml.3*
%endif

%if %{with perl}
%files -n perl-libguestfs
%defattr(644,root,root,755)
%{perl_vendorarch}/Sys/Guestfs.pm
%dir %{perl_vendorarch}/Sys/Guestfs
%{perl_vendorarch}/Sys/Guestfs/Lib.pm
%{perl_vendorarch}/Sys/bindtests.pl
%dir %{perl_vendorarch}/auto/Sys/Guestfs
%{perl_vendorarch}/auto/Sys/Guestfs/Guestfs.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Sys/Guestfs/Guestfs.so
%{_mandir}/man3/guestfs-perl.3*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/Sys::Guestfs::Lib.3pm*
%lang(ja) %{_mandir}/ja/man3/guestfs-perl.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-perl.3*
%endif

%if %{with php}
%files -n php-guestfs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php/conf.d/guestfs_php.ini
%attr(755,root,root) %{_libdir}/php/guestfs_php.so
%endif

%if %{with python}
%files -n python-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libguestfsmod.so
%{py_sitedir}/guestfs.py[co]
%{_mandir}/man3/guestfs-python.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-python.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-python.3*
%endif

%if %{with ruby}
%files -n ruby-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_sitearchdir}/_guestfs.so
%{ruby_sitelibdir}/guestfs.rb
%{_mandir}/man3/guestfs-ruby.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-ruby.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-ruby.3*
%endif

%files -n bash-completion-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) /etc/bash_completion.d/guestfish-bash-completion.sh
