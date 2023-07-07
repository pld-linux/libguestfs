# TODO:
# - finish haskell bindings (when finished upstream, not ready as of 1.30.4)
# - PLD appliance support? (needs at least package list adjustment)
#
# Conditional build:
%bcond_with	static_libs	# build static libraries
%bcond_with	appliance	# appliance build (no PLD support)
%bcond_without	erlang		# Erlang binding
%bcond_with	golang		# Go language binding
%bcond_with	haskell		# Haskell (GHC) binding [incomplete, nothing is installed]
%bcond_with	java		# Java binding (broken linking, missing symbols)
%bcond_without	lua		# Lua binding
%bcond_without	ocaml		# OCaml binding and tools
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)
%bcond_without	perl		# Perl binding
%bcond_with	php		# PHP binding
%bcond_without	python		# Python binding
%bcond_without	ruby		# Ruby binding
%bcond_with	rust		# Rust binding
%bcond_without	vala		# vala binding

%if 0%{!?php_name:1}
%define		php_name	php55
%endif

%ifarch x32
%undefine	with_erlang
%undefine	with_ocaml_opt
%endif

%ifnarch %{go_arches}
%undefine	with_golang
%endif

%{?with_java:%{?use_default_jdk}}

Summary:	Library and tools for accessing and modifying virtual machine disk images
Summary(pl.UTF-8):	Biblioteka i narzędzia do dostępu i modyfikacji obrazów dysków maszyn wirtualnych
Name:		libguestfs
Version:	1.50.1
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	https://libguestfs.org/download/1.50-stable/%{name}-%{version}.tar.gz
# Source0-md5:	eea08678d34a856dea49ef688634a341
Patch0:		ncurses.patch
Patch1:		augeas-libxml2.patch
Patch2:		%{name}-completionsdir.patch
Patch3:		x32.patch
Patch4:		appliance-pld.patch
URL:		https://libguestfs.org/
BuildRequires:	acl-devel
BuildRequires:	augeas-devel >= 1.2.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cdrkit-mkisofs
BuildRequires:	cpio
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gperf
BuildRequires:	hivex-devel >= 1.2.7
BuildRequires:	jansson-devel >= 2.7
BuildRequires:	libcap-devel
BuildRequires:	libconfig-devel
BuildRequires:	libfuse-devel
BuildRequires:	libmagic-devel
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtirpc-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libvirt-devel >= 0.10.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxml2-progs
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= 1:4.04
BuildRequires:	ocaml-augeas-devel
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-hivex-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	perl-base
BuildRequires:	perl-libintl
BuildRequires:	perl-modules
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	po4a
BuildRequires:	qemu-img >= 1.3.0
BuildRequires:	readline-devel
BuildRequires:	rpcsvc-proto
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel >= 4.6.0
BuildRequires:	rpmbuild(macros) >= 2.021
BuildRequires:	sleuthkit-devel
# libsystemd-journal
BuildRequires:	systemd-devel >= 1:196
%{?with_vala:BuildRequires:	vala}
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	yara-devel >= 4.0.0
BuildRequires:	zstd
%if %{with appliance}
BuildRequires:	supermin >= 5.2.2-2
%endif
%if %{with erlang}
# erl_interface package
BuildRequires:	erlang
%endif
%if %{with golang}
BuildRequires:	golang
%endif
%if %{with haskell}
BuildRequires:	ghc
%endif
%if %{with java}
%buildrequires_jdk
BuildRequires:	rpm-javaprov
%endif
%if %{with lua}
BuildRequires:	lua
BuildRequires:	lua-devel
%endif
%if %{with ocaml}
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-fileutils-devel
BuildRequires:	ocaml-gettext-devel
BuildRequires:	ocaml-libvirt-devel >= 0.6.1.4-4
BuildRequires:	ocaml-pcre-devel
%endif
%if %{with perl}
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Module-Build
BuildRequires:	perl-Test-Simple
BuildRequires:	rpm-perlprov
%endif
%if %{with php}
BuildRequires:	%{php_name}-devel
BuildRequires:	%{php_name}-program
%endif
%if %{with python}
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	rpm-pythonprov
%endif
%if %{with ruby}
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-irb
BuildRequires:	ruby-rake
BuildRequires:	ruby-rdoc
BuildRequires:	ruby-rubygems
%endif
%if %{with rust}
BuildRequires:	cargo
BuildRequires:	rust
%endif
Requires:	jansson >= 2.7
Requires:	qemu-common >= 1.3.0
Requires:	yajl >= 2.0.4
Suggests:	db-utils
Suggests:	icoutils
Suggests:	netpbm-progs
Obsoletes:	libguestfs-apidocs < 1.40.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		qemu_bin	/usr/bin/qemu-system-i386
%endif
%ifarch %{x8664} x32
%define		qemu_bin	/usr/bin/qemu-system-x86_64
%endif
%ifarch aarch64
%define		qemu_bin	/usr/bin/qemu-system-aarch64
%endif
%ifarch %{arm}
%define		qemu_bin	/usr/bin/qemu-system-arm
%endif

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
Requires:	augeas-libs >= 1.2.0
%{?with_ocaml:Requires:	ocaml-libguestfs = %{version}-%{release}}
%if %{with ocaml}
Requires:	ocaml-libvirt >= 0.6.1.4-4
Suggests:	unzip
Suggests:	xz
Suggests:	zip
%endif

%description tools
libguestfs tools for accessing and modifying virtual machine (VM) disk
images. You can use this for viewing and editing files inside guests,
scripting changes to VMs, monitoring disk used/free statistics,
performing partial backups, cloning VMs, and much else besides.

%description tools -l pl.UTF-8
Zestaw narzędzi libguestfs do dostępu oraz modyfikowania obrazów
dysków maszyn wirtualnych (VM). Można je wykorzystywać do oglądania i
edycji plików wewnątrz gości, zmian skryptowych w VM-ach,
monitorowania statystyk używanego/dostępnego miejsca na dyskach,
wykonywania częściowych kopii zapasowych, klonowania VM-ów i wielu
podobnych operacji.

%package -n erlang-libguestfs
Summary:	Erlang bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Erlanga do libguestfs
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n erlang-libguestfs
Erlang bindings for libguestfs.

%description -n erlang-libguestfs -l pl.UTF-8
Wiązania Erlanga do libguestfs.

%package -n golang-libguestfs
Summary:	Go language bindings for libguestfs
Summary(pl.UTF-8):	Wiązania języka Go do libguestfs
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n golang-libguestfs
Go language bindings for libguestfs.

%description -n golang-libguestfs -l pl.UTF-8
Wiązania języka Go do libguestfs.

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

%package -n %{php_name}-guestfs
Summary:	PHP bindings for libguestfs
Summary(pl.UTF-8):	Wiązania PHP do libguestfs
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-guestfs
PHP bindings for libguestfs.

%description -n %{php_name}-guestfs -l pl.UTF-8
Wiązania PHP do libguestfs.

%package -n python3-libguestfs
Summary:	Python bindings for libguestfs
Summary(pl.UTF-8):	Wiązania Pythona do libguestfs
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-libguestfs < 1.46

%description -n python3-libguestfs
Python bindings for libguestfs.

%description -n python3-libguestfs -l pl.UTF-8
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

%package -n vala-libguestfs
Summary:	Vala bindings for libguestfs
Summary(pl.UTF-8):	Wiązania języka Vala do libguestfs
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description -n vala-libguestfs
Vala bindings for libguestfs.

%description -n vala-libguestfs -l pl.UTF-8
Wiązania języka Vala do libguestfs.

%package -n bash-completion-libguestfs
Summary:	bash-completion for libguestfs tools
Summary(pl.UTF-8):	Bashowe uzupełnianie argumentów dla narzędzi libguestfs
Group:		Applications/Shells
Requires:	%{name}-tools = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-libguestfs
bash-completion for libguestfs tools.

%description -n bash-completion-libguestfs -l pl.UTF-8
Bashowe uzupełnianie argumentów dla narzędzi libguestfs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifarch x32
%patch3 -p1
%endif
%patch4 -p1

%build
# preserve dir across libtoolize
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	vmchannel_test=no \
	DB_DUMP=/usr/bin/db_dump \
	DB_LOAD=/usr/bin/db_load \
	PBMTEXT=/usr/bin/pbmtext \
	PNMTOPNG=/usr/bin/pnmtopng \
	BMPTOPNM=/usr/bin/bmptopnm \
	PAMCUT=/usr/bin/pamcut \
	SUPERMIN=/usr/bin/supermin \
	UNZIP=/usr/bin/unzip \
	WRESTOOL=/usr/bin/wrestool \
	QEMU=%{?qemu_bin}%{!?qemu_bin:/usr/bin/qemu} \
	ZIP=/usr/bin/zip \
	PYTHON=%{__python3} \
	--with-completionsdir=%{bash_compdir} \
	--with-java=%{?with_java:%{java_home}}%{!?with_java:no} \
	--with-python-installdir=%{py3_sitedir} \
	--enable-install-daemon \
	%{!?with_appliance:--disable-appliance} \
	%{!?with_erlang:--disable-erlang} \
	%{!?with_golang:--disable-golang} \
	%{!?with_haskell:--disable-haskell} \
	%{!?with_lua:--disable-lua} \
	%{!?with_ocaml:--disable-ocaml} \
	%{!?with_perl:--disable-perl} \
	%{!?with_php:--disable-php} \
	%{!?with_python:--disable-python} \
	%{!?with_ruby:--disable-ruby} \
	%{!?with_rust:--disable-rust} \
	%{!?with_vala:--disable-vala} \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make} -j1 \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT \
	phpdir=%{php_sysconfdir}/conf.d

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%if %{with lua}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lua/*/*.la
%endif
%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%if %{without appliance}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{ja,uk}/man1/libguestfs-make-fixed-appliance.1
%endif
%if %{without golang}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{ja,uk}/man3/guestfs-golang.3
%endif
%if %{without java}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{ja,uk}/man3/guestfs-java.3
%endif
%if %{with ocaml}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/dll*.so.owner
%else
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{ja,uk}/man3/guestfs-ocaml.3
%endif
%if %{without ruby}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{ja,uk}/man3/guestfs-ruby.3
%endif
# useless in binary package
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{man1,ja/man1,uk/man1}/guestfs-building.1

install -d $RPM_BUILD_ROOT%{_libdir}/guestfs

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
%doc AUTHORS README TODO
%attr(755,root,root) %{_libdir}/libguestfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguestfs.so.0
%dir %{_libdir}/guestfs
%{_mandir}/man1/guestfs-release-notes*.1*
%{_mandir}/man1/guestfs-security.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-release-notes*.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-security.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-release-notes*.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-security.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguestfs.so
%{_includedir}/guestfs.h
%{_pkgconfigdir}/libguestfs.pc
%{_mandir}/man1/guestfs-hacking.1*
%{_mandir}/man1/guestfs-internals.1*
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/libguestfs.3*
%lang(ja) %{_mandir}/ja/man1/guestfs-hacking.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-internals.1*
%lang(ja) %{_mandir}/ja/man3/guestfs.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-examples.3*
%lang(uk) %{_mandir}/uk/man1/guestfs-hacking.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-internals.1*
%lang(uk) %{_mandir}/uk/man3/guestfs.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-examples.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libguestfs.a
%endif

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
%{_mandir}/man3/guestfs-gobject.3*

%if %{with static_libs}
%files gobject-static
%defattr(644,root,root,755)
%{_libdir}/libguestfs-gobject-1.0.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/guestfish
%attr(755,root,root) %{_bindir}/guestmount
%attr(755,root,root) %{_bindir}/guestunmount
%attr(755,root,root) %{_bindir}/libguestfs-test-tool
%attr(755,root,root) %{_bindir}/virt-copy-in
%attr(755,root,root) %{_bindir}/virt-copy-out
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
%{_mandir}/man1/guestunmount.1*
%{_mandir}/man1/libguestfs-test-tool.1*
%{_mandir}/man1/virt-copy-in.1*
%{_mandir}/man1/virt-copy-out.1*
%{_mandir}/man1/virt-rescue.1*
%{_mandir}/man1/virt-tar-in.1*
%{_mandir}/man1/virt-tar-out.1*
%{_mandir}/man5/libguestfs-tools.conf.5*
%{_mandir}/man8/guestfsd.8*
%lang(ja) %{_mandir}/ja/man1/guestfish.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-faq.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-performance.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-recipes.1*
%lang(ja) %{_mandir}/ja/man1/guestfs-testing.1*
%lang(ja) %{_mandir}/ja/man1/guestmount.1*
%lang(ja) %{_mandir}/ja/man1/guestunmount.1*
%lang(ja) %{_mandir}/ja/man1/libguestfs-test-tool.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-copy-out.1*
%lang(ja) %{_mandir}/ja/man1/virt-rescue.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-in.1*
%lang(ja) %{_mandir}/ja/man1/virt-tar-out.1*
%lang(ja) %{_mandir}/ja/man5/libguestfs-tools.conf.5*
%lang(uk) %{_mandir}/uk/man1/guestfish.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-faq.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-performance.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-recipes.1*
%lang(uk) %{_mandir}/uk/man1/guestfs-testing.1*
%lang(uk) %{_mandir}/uk/man1/guestmount.1*
%lang(uk) %{_mandir}/uk/man1/guestunmount.1*
%lang(uk) %{_mandir}/uk/man1/libguestfs-test-tool.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-copy-out.1*
%lang(uk) %{_mandir}/uk/man1/virt-rescue.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-in.1*
%lang(uk) %{_mandir}/uk/man1/virt-tar-out.1*
%lang(uk) %{_mandir}/uk/man5/libguestfs-tools.conf.5*

%if %{with appliance}
%attr(755,root,root) %{_sbindir}/libguestfs-make-fixed-appliance
%{_mandir}/man1/libguestfs-make-fixed-appliance.1*
%lang(ja) %{_mandir}/ja/man1/libguestfs-make-fixed-appliance.1*
%lang(uk) %{_mandir}/uk/man1/libguestfs-make-fixed-appliance.1*
/lib/udev/rules.d/99-guestfs-serial.rules
%dir %{_libdir}/guestfs
%dir %{_libdir}/guestfs/supermin.d
%{_libdir}/guestfs/supermin.d/base.tar.gz
%{_libdir}/guestfs/supermin.d/daemon.tar.gz
%{_libdir}/guestfs/supermin.d/excludefiles
%{_libdir}/guestfs/supermin.d/hostfiles
%{_libdir}/guestfs/supermin.d/init.tar.gz
%{_libdir}/guestfs/supermin.d/packages
%{_libdir}/guestfs/supermin.d/udev-rules.tar.gz
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

%if %{with golang}
%files -n golang-libguestfs
%defattr(644,root,root,755)
%dir %{_libdir}/golang/pkg/linux_*/libguestfs.org
%dir %{_libdir}/golang/pkg/linux_*/libguestfs.org/guestfs
%{_libdir}/golang/pkg/linux_*/libguestfs.org/guestfs/guestfs.a
%{_libdir}/golang/src/libguestfs.org
%{_mandir}/man3/guestfs-golang.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-golang.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-golang.3*
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
%{_javadocdir}/libguestfs
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
%dir %{_libdir}/ocaml/guestfs
%{_libdir}/ocaml/guestfs/META
%{_libdir}/ocaml/guestfs/mlguestfs.cma

%files -n ocaml-libguestfs-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/guestfs/guestfs.cmi
%{_libdir}/ocaml/guestfs/guestfs.mli
%{_libdir}/ocaml/guestfs/libmlguestfs.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/guestfs/guestfs.cmx
%{_libdir}/ocaml/guestfs/mlguestfs.a
%{_libdir}/ocaml/guestfs/mlguestfs.cmxa
%endif
%{_mandir}/man3/guestfs-ocaml.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-ocaml.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-ocaml.3*
%endif

%if %{with perl}
%files -n perl-libguestfs
%defattr(644,root,root,755)
%{perl_vendorarch}/Sys/Guestfs.pm
%dir %{perl_vendorarch}/auto/Sys/Guestfs
%attr(755,root,root) %{perl_vendorarch}/auto/Sys/Guestfs/Guestfs.so
%{_mandir}/man3/guestfs-perl.3*
%{_mandir}/man3/Sys::Guestfs.3pm*
%lang(ja) %{_mandir}/ja/man3/guestfs-perl.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-perl.3*
%endif

%if %{with php}
%files -n %{php_name}-guestfs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/guestfs_php.ini
%attr(755,root,root) %{php_extensiondir}/guestfs_php.so
%endif

%if %{with python}
%files -n python3-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/libguestfsmod*.so
%{py3_sitedir}/guestfs.py
%{py3_sitedir}/__pycache__
%{_mandir}/man3/guestfs-python.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-python.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-python.3*
%endif

%if %{with ruby}
%files -n ruby-libguestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/_guestfs.so
%{ruby_vendorlibdir}/guestfs.rb
%{_mandir}/man3/guestfs-ruby.3*
%lang(ja) %{_mandir}/ja/man3/guestfs-ruby.3*
%lang(uk) %{_mandir}/uk/man3/guestfs-ruby.3*
%endif

%if %{with vala}
%files -n vala-libguestfs
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libguestfs-gobject-1.0.deps
%{_datadir}/vala/vapi/libguestfs-gobject-1.0.vapi
%endif

%files -n bash-completion-libguestfs
%defattr(644,root,root,755)
%{bash_compdir}/guestfish
%{bash_compdir}/guestmount
%{bash_compdir}/guestunmount
%{bash_compdir}/libguestfs-test-tool
%{bash_compdir}/virt-*
