#
# Conditional build:
%bcond_with		verbose		# verbose build (V=1)

# TODO
# - https://developers.google.com/speed/pagespeed/psol
# - build using system libs:
#  - gflags
#  - giflib
#  - gtest
#  - icu
#  - libharu
#  - libjpeg
#  - libpng
#  - libwebp
#  - optipng
#  - protobuf
#  - zlib
#  . ...
Summary:	Page Speed native libraries
Name:		libpagespeed
Version:	1.12.16.0
Release:	0.2
License:	Apache v2.0
Group:		Libraries
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	59922b57b304392a9364bb659ffc7d2c
Source1:	get-source.sh
Source2:	gclient.conf
URL:		https://code.google.com/p/page-speed/
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Page Speed library, a reusable C++ library that provides the core
Page Speed rule logic.

%prep
%setup -q

%build
test %{_specdir}/%{name}.spec -nt Makefile && %{__rm} -f Makefile
test -e Makefile || \
CC="%{__cc}" \
CXX="%{__cxx}" \
%{__python} build/gyp_chromium \
	--format=make \
	--depth=. \
	build/all.gyp \
	-Duse_openssl=1 \
	-Duse_system_icu=0 \
	-Duse_system_libjpeg=1 \
	-Duse_system_libpng=1 \
	-Duse_system_ssl=1 \
	-Duse_system_zlib=1 \
	%{nil}

%{__make} -r \
	BUILDTYPE=%{!?debug:Release}%{?debug:Debug} \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CC.host="%{__cc}" \
	CXX.host="%{__cxx}" \
	LINK.host="%{__cxx}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	%{nil}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}

cd out/%{!?debug:Release}%{?debug:Debug}

for a in *_bin; do
	install -p $a $RPM_BUILD_ROOT%{_bindir}/${a%_bin}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/minify_css
%attr(755,root,root) %{_bindir}/minify_html
%attr(755,root,root) %{_bindir}/minify_js
%attr(755,root,root) %{_bindir}/optimize_image
%attr(755,root,root) %{_bindir}/pagespeed
