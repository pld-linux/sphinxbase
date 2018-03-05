#
# Conditional build:
%bcond_without	python		# Python extension
%bcond_without	static_libs	# static libraries
%bcond_with	tests		# "make check" [unit/test_ngram/test_lm_mmap fails]

Summary:	CMU Sphinx common libraries
Summary(pl.UTF-8):	Wspólne biblioteki CMU Sphinx
Name:		sphinxbase
Version:	0.8
Release:	1
License:	BSD
Group:		Applications/Communications
Source0:	http://downloads.sourceforge.net/cmusphinx/%{name}-%{version}.tar.gz
# Source0-md5:	7335d233f7ad4ecc4b508aec7b5dc101
Patch0:		%{name}-am.patch
URL:		https://cmusphinx.github.io/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	doxygen
BuildRequires:	lapack-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
# pulse > jack > alsa > oss (in the order of priority, only one can be enabled)
BuildRequires:	pulseaudio-devel
%if %{with python}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 2.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the basic libraries shared by the CMU Sphinx
trainer and all the Sphinx decoders (Sphinx-II, Sphinx-III, and
PocketSphinx), as well as some common utilities for manipulating
acoustic feature and audio files.

%description -l pl.UTF-8
Ten pakiet zawiera podstawowe biblioteki współdzielone przez trenera
CMU Sphinx oraz wszystkie dekodery (Sphinx-II, Sphinx-III oraz
PocketSphinx), a także trochę wspólnych narzędzi do operowania na
plikach dźwiękowych oraz danych akustycznych.

%package devel
Summary:	Header files for CMU Sphinx common libraries
Summary(pl.UTF-8):	Pliki nagłówkowe wspólnych bibliotek CMU Sphinx
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Requires:	lapack-devel
Requires:	libsamplerate-devel
Requires:	libsndfile-devel
Requires:	pulseaudio-devel

%description devel
Header files for CMU Sphinx common libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe wspólnych bibliotek CMU Sphinx.

%package static
Summary:	Static CMU Sphinx common libraries
Summary(pl.UTF-8):	Statyczne biblioteki wspólne CMU Sphinx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CMU Sphinx common libraries.

%description static -l pl.UTF-8
Statyczne biblioteki wspólne CMU Sphinx.

%package -n python-sphinxbase
Summary:	Python interface to CMU Sphinx base libraries
Summary(pl.UTF-8):	Interfejs Pythona do podstawowych bibliotek CMU Sphinx
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-sphinxbase
Python interface to CMU Sphinx base libraries.

%description -n python-sphinxbase -l pl.UTF-8
Interfejs Pythona do podstawowych bibliotek CMU Sphinx.

%package -n python-sphinxbase-devel
Summary:	Header file for Python interface to CMU Sphinx base libraries
Summary(pl.UTF-8):	Plik nagłówkowy interfejsu Pythona do podstawowych bibliotek CMU Sphinx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-sphinxbase = %{version}-%{release}
Requires:	python-devel >= 2.0

%description -n python-sphinxbase-devel
Header file for Python interface to CMU Sphinx base libraries.

%description -n python-sphinxbase-devel -l pl.UTF-8
Plik nagłówkowy interfejsu Pythona do podstawowych bibliotek CMU
Sphinx.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env perl,/usr/bin/perl,' src/sphinx_lmtools/sphinx_lm_sort

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_python:--without-python} \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsphinx*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc
%attr(755,root,root) %{_bindir}/sphinx_cepview
%attr(755,root,root) %{_bindir}/sphinx_cont_adseg
%attr(755,root,root) %{_bindir}/sphinx_cont_fileseg
%attr(755,root,root) %{_bindir}/sphinx_fe
%attr(755,root,root) %{_bindir}/sphinx_jsgf2fsg
%attr(755,root,root) %{_bindir}/sphinx_lm_convert
%attr(755,root,root) %{_bindir}/sphinx_lm_eval
%attr(755,root,root) %{_bindir}/sphinx_lm_sort
%attr(755,root,root) %{_bindir}/sphinx_pitch
%attr(755,root,root) %{_libdir}/libsphinxad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsphinxad.so.0
%attr(755,root,root) %{_libdir}/libsphinxbase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsphinxbase.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsphinxad.so
%attr(755,root,root) %{_libdir}/libsphinxbase.so
%dir %{_includedir}/sphinxbase
%{_includedir}/sphinxbase/*.h
%{_pkgconfigdir}/sphinxbase.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsphinxad.a
%{_libdir}/libsphinxbase.a
%endif

%if %{with python}
%files -n python-sphinxbase
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/sphinxbase.so
%{py_sitedir}/SphinxBase-%{version}-py*.egg-info

%files -n python-sphinxbase-devel
%defattr(644,root,root,755)
%{_includedir}/sphinxbase/sphinxbase.pxd
%endif
