Summary:	GObject-introspection based JavaScript bindings
Name:		gjs
Version:	1.38.1
Release:	1
License:	MPL1.1/LGPLv2+/GPLv2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gjs/1.38/%{name}-%{version}.tar.xz
# Source0-md5:	0f3422a114cb69735274e75e325013a3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	js-devel >= 17.0.0
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GObject-introspection based JavaScript bindings.

%package libs
Summary:	GJS libraries
Group:		Libraries

%description libs
GJS libraries.

%package devel
Summary:	Header files for GJS library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for GJS library.

%prep
%setup -q
# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gjs-1.0/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/gjs-1.0

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/gjs
%dir %{_libdir}/gjs/girepository-1.0
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/gjs/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/gjs-1.0
%{_pkgconfigdir}/*.pc

