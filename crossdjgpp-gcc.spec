Summary:	DJGPP GNU Binary Utility Development Utilities - gcc
Name:		crossdjgpp-gcc
Version:	3.0.2
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Source0:	ftp://ftp.gnu.org/pub/gnu/gcc-%{version}-20011014.tar.gz
BuildRequires:	crossdjgpp-platform
BuildRequires:	crossdjgpp-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	/bin/bash
Requires:	crossdjgpp-binutils
Requires:	crossdjgpp-platform
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cxx		0
%define		target		i386-pc-msdosdjgpp
%define		_prefix		/usr
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%description
DJGPP is a port of GNU GCC to the DOS environment. (It stands for
DJ's Gnu Programming Platform, if it has to stand for something, but
it's best left ambiguous.)

This package contains cross targeted gcc.

%if %{cxx}
%package c++
Summary:	DJGPP GNU Binary Utility Development Utilities - g++
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Requires:	%{name} = %{version}

%description c++
DJGPP is a port of GNU GCC to the DOS environment. (It stands for
DJ's Gnu Programming Platform, if it has to stand for something, but
it's best left ambiguous.)

This package contains cross targeted g++ and (static) libstdc++.
%endif

# does this even work?
%package g77
Summary:	DJGPP GNU Binary Utility Development Utilities - g77
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Requires:	%{name} = %{version}

%description g77
DJGPP is a port of GNU GCC to the DOS environment. (It stands for
DJ's Gnu Programming Platform, if it has to stand for something, but
it's best left ambiguous.)

This package contains cross targeted g77.

%prep
%setup -q -n gcc-%{version}-20011014

%build
rm -rf obj-%{target} 
install -d obj-%{target}
cd obj-%{target} 

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--disable-shared \
	--enable-haifa \
        --enable-languages="c,f77,gcov" \
	--enable-long-long \
	--enable-namespaces \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-x \
	--target=%{target}

# kluge, we already have full system headers and libraries ready,
# needed to get right limits.h
cd gcc
cp Makefile Makefile.new
sed -e "s|^SYSTEM_HEADER_DIR.*|SYSTEM_HEADER_DIR := /usr/%{target}/include|" \
	Makefile.new > Makefile
rm -f Makefile.new
cd ..

# YAK (Yet Another Kluge) :<
cd ../libstdc++-v3
cp configure configure.tmp
# don't use newlib, we want djgpp
sed -e 's|os_include_dir="config/os/newlib"|#&|' configure.tmp > configure
cd ../obj-%{target}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
#LDFLAGS_FOR_TARGET="%{rpmldflags}"

%{__make} -C obj-%{target}
	
#%{__make} -C obj-%{target}/gcc \
#	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
#	mandir=%{_mandir} \
#	infodir=%{_infodir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir},%{_bindir}}

cd obj-%{target}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} -C gcc install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	gxx_include_dir=$RPM_BUILD_ROOT%{arch}/include/g++ \
	DESTDIR=$RPM_BUILD_ROOT

# c++filt is provided by binutils
#rm -f $RPM_BUILD_ROOT%{_bindir}/i386-djgpp-c++filt

# what is this there for???
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# the same... make hardlink
#ln -f $RPM_BUILD_ROOT%{arch}/bin/gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc

%{target}-strip -g $RPM_BUILD_ROOT/%{gcclib}/libgcc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
#%dir %{arch}/bin
#%attr(755,root,root) %{arch}/bin/cpp
#%attr(755,root,root) %{arch}/bin/gcc
#%attr(755,root,root) %{arch}/bin/gcov
#%{arch}/include/_G_config.h
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/tradcpp0
%attr(755,root,root) %{gcclib}/cpp0
%attr(755,root,root) %{gcclib}/collect2
#%{gcclib}/SYSCALLS.c.X
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
#%{gcclib}/include/iso646.h
#%{gcclib}/include/limits.h
#%{gcclib}/include/proto.h
#%{gcclib}/include/stdarg.h
#%{gcclib}/include/stdbool.h
#%{gcclib}/include/stddef.h
#%{gcclib}/include/syslimits.h
#%{gcclib}/include/varargs.h
#%{gcclib}/include/va-*.h
%{_mandir}/man1/%{target}-gcc.1*

%if %{cxx}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-[cg]++
%{arch}/include/g++
%{arch}/lib/libstdc++.a
%attr(755,root,root) %{gcclib}/cc1plus
%{gcclib}/libstdc++*
%{gcclib}/include/new.h
%{gcclib}/include/exception
%{gcclib}/include/new
%{gcclib}/include/typeinfo
%{_mandir}/man1/%{target}-g++.1*
%endif

%files g77
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g77
%attr(755,root,root) %{gcclib}/f771
%{_mandir}/man1/%{target}-g77.1*
