#
# Conditional build:
%bcond_without	wx	# wxWidgets-based player
#
Summary:	C++ library for high quality time stretching and pitch scaling
Summary(pl.UTF-8):	Biblioteka C++ do wysokiej jakości zmiany szybkości i wysokości dźwięku
Name:		libsbsms
Version:	1.7.0
Release:	3
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sbsms/%{name}-%{version}.tar.gz
# Source0-md5:	6a6d1549fe4c4c7de8bfff5ce13bdece
Patch0:		%{name}-opts.patch
Patch1:		%{name}-gcc.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-mad.patch
URL:		http://sbsms.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.5
BuildRequires:	libmad-devel
BuildRequires:	libsndfile-devel >= 1.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	portaudio-devel >= 19
BuildRequires:	pkgconfig
%{?with_wx:BuildRequires:	wxGTK2-unicode-devel >= 2.8}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsbsms is a library for high quality time and pitch scale
modification. It uses octave subband sinusoidal modeling.

%description -l pl.UTF-8
libsbsms to biblioteka do wysokiej jakości modyfikowania szybkości i
wysokości dźwięku. Wykorzystuje modelowanie sinusoidalne.

%package devel
Summary:	Header files for libsbsms library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsbsms
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for libsbsms library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsbsms.

%package static
Summary:	Static libsbsms library
Summary(pl.UTF-8):	Statyczna biblioteka libsbsms
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsbsms library.

%description static -l pl.UTF-8
Statyczna biblioteka libsbsms.

%package wx
Summary:	wxWidgets-based player
Summary(pl.UTF-8):	Odtwarzacz oparty na wxWidgets
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description wx
wxWidgets-based player utilizing libsbsms.

%description wx -l pl.UTF-8
Oparty na wxWidgets odtwarzacz wykorzystujący libsbsms.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	WX_CONFIG=/usr/bin/wx-gtk2-unicode-config \
	--enable-mp3 \
	--enable-multithreaded \
	--enable-portaudio \
	--enable-sndfile \
	--enable-shared \
	%{?with_wx:--enable-wx}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/sbsms
%attr(755,root,root) %{_bindir}/sbsmsplay
%attr(755,root,root) %{_libdir}/libsbsms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsbsms.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsbsms.so
%{_libdir}/libsbsms.la
%{_includedir}/sbsms.h
%{_pkgconfigdir}/sbsms.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsbsms.a

%if %{with wx}
%files wx
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wxsbsmsplayer
%endif
