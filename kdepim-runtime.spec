%define akonadi_version 1.2.1

Name: kdepim-runtime
Summary: KDE PIM Runtime Environment
Version: 4.3.4
Release: 4%{?dist}.0.sl6

License: GPLv2
Group: Applications/Productivity
Url: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# 4.3 branch fixes
Patch100: kdepim-runtime-4.3.5.patch

# fix build issue without webkit 
Patch200: kdepim-runtime-4.3.4-nowebkit.patch


Requires: %{name}-libs = %{version}-%{release}

BuildRequires: akonadi-devel >= %{akonadi_version}
BuildRequires: desktop-file-utils
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: kdelibs-experimental-devel >= %{version}
BuildRequires: zlib-devel
BuildRequires: soprano-devel
BuildRequires: libxslt-devel
BuildRequires: libxml2-devel

%description
%{summary}


%package libs
Summary: %{name} runtime libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: akonadi%{?_isa} >= %{akonadi_version}

%description libs
%{summary}.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: kdepimlibs-devel

%description devel
%{summary}.
Install %{name}-devel if you want to write or compile %{name} plugins.


%prep
%setup -q

# 4.3 branch
%patch100 -p1 -b .kde435
# fix build issue without webkit 
%patch200 -p1 -b .nowebkit

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# make symlinks relative
mkdir -p %{buildroot}%{_docdir}/HTML/en/common
pushd %{buildroot}%{_docdir}/HTML/en
for i in *; do
   if [ -d $i -a -L $i/common ]; then
      rm -f $i/common
      ln -nfs ../common $i
   fi
done
popd

%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
   desktop-file-validate $f
done

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime >& /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  update-mime-database %{_kde4_datadir}/mime &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_kde4_bindir}/*
%{_kde4_libdir}/kde4/*.so
%{_kde4_datadir}/akonadi/agents/*
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/config/*rc
%{_kde4_datadir}/dbus-1/interfaces/*.xml
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/mime/packages/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_appsdir}/*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/akonadi/xml/
%{_kde4_libdir}/lib*.so

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*


%changelog
* Wed Dec 22 2010 Troy Dawson <dawson@fnal.gov> - 4.3.4-4.0.sl6
- Added patch required to build with the webkit (bz#660581)

* Wed Mar 31 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- rebuilt against qt 4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- backport 4.3.5 fixes

* Thu Dec 31 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- fix source path

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Sat Jul 11 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Thu Jul 02 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.95-3
- -devel: Requires: kdepimlibs-devel
- Req: akonadi >= 1.1.95

* Mon Jun 29 2009 Than Ngo <than@redhat.com> - 4.2.95-2
- cleanup

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- first try
