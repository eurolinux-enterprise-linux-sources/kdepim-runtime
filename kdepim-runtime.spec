%global akonadi_version_min 1.9.0
%global akonadi_version %(pkg-config --modversion akonadi 2>/dev/null || echo %{akonadi_version_min})

Name:    kdepim-runtime
Summary: KDE PIM Runtime Environment
Epoch:   1
Version: 4.10.5
Release: 1%{?dist}

License: GPLv2
URL: http://www.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

# show the Akonadi KCM in System Settings (#565420)
Patch0: kdepim-runtime-4.4.93-show_akonadi_kcm.patch

## upstreamable patches

## upstream patches

# nuke ill-advised -devel pkg
Obsoletes: kdepim-runtime-devel < 1:4.7.90-3

Provides: kdepim4-runtime = %{version}-%{release}

Obsoletes: akonadi-google < 0.4
Provides:  akonadi-google = %{version}-%{release}
Obsoletes: akonadi-google-calendar < 0.4
Provides:  akonadi-google-calendar = %{version}-%{release}
Obsoletes: akonadi-google-contacts < 0.4
Provides:  akonadi-google-contacts = %{version}-%{release}
Obsoletes: akonadi-google-tasks < 0.4
Provides:  akonadi-google-tasks = %{version}-%{release}

Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version} 
BuildRequires: nepomuk-core-devel >= %{version}
%if 0%{?fedora}
BuildRequires: libkolab-devel
BuildRequires: pkgconfig(libkgapi)
%endif
BuildRequires: pkgconfig(akonadi) >= %{akonadi_version_min}
BuildRequires: pkgconfig(libstreamanalyzer) pkgconfig(libstreams)
BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(QJson)
BuildRequires: pkgconfig(shared-desktop-ontologies) >= 0.10
BuildRequires: pkgconfig(soprano)
BuildRequires: pkgconfig(zlib)

%description
%{summary}.

%package libs
Summary: %{name} runtime libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: akonadi%{?_isa} >= %{akonadi_version}
%{?_kde4_version:Requires: kdepimlibs-akonadi%{?_isa} >= %{_kde4_version}}
%description libs
%{summary}.


%prep
%setup -q -n kdepim-runtime-%{version}%{?pre}

%patch0 -p1 -b .show_akonadi_kcm


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -fv %{buildroot}%{_kde4_libdir}/lib{akonadi-filestore,akonadi-xml,kdepim-copy,kmindexreader,maildir}.so
rm -fv %{buildroot}%{_kde4_libdir}/libnepomukfeederpluginlib.a


%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
   desktop-file-validate $f
done


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime >& /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
  update-mime-database %{_kde4_datadir}/mime &> /dev/null ||:
fi

%files 
%{_kde4_bindir}/*
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/kde4/imports/*
%{_kde4_datadir}/akonadi/agents/*
%{_kde4_datadir}/applications/kde4/*.desktop
%{_kde4_datadir}/autostart/kaddressbookmigrator.desktop
%{_kde4_datadir}/config/*rc
%{_kde4_datadir}/dbus-1/interfaces/*.xml
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/services/*.protocol
%{_kde4_datadir}/kde4/services/akonadi/davgroupware-providers/
%{_kde4_datadir}/kde4/services/kresources/kabc/*.desktop
%{_kde4_datadir}/kde4/services/kresources/kcal/*.desktop
%{_kde4_datadir}/kde4/servicetypes/*.desktop
%{_kde4_datadir}/mime/packages/*.xml
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_appsdir}/akonadi/
%{_kde4_appsdir}/akonadi_knut_resource/
%{_kde4_appsdir}/akonadi_maildispatcher_agent/
%{_kde4_appsdir}/akonadi_nepomuk_feeder/
%{_kde4_appsdir}/nepomukpimindexerutility/

%dir %{_datadir}/ontology/kde/
%{_datadir}/ontology/kde/aneo.*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/libakonadi-filestore.so.4*
%{_kde4_libdir}/libakonadi-xml.so.4*
%{_kde4_libdir}/libkdepim-copy.so.4*
%{_kde4_libdir}/libkmindexreader.so.4*
%{_kde4_libdir}/libmaildir.so.4*


%changelog
* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sun Jun 02 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.10.4-1.2
- rebuild (libkgapi)

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.10.4-1
- 4.10.4

* Wed May 22 2013 Daniel Vrátil <dvratil@redhat.com> 1:4.10.3-3
- Rebuild for libkgapi-2.0.0

* Fri May 10 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.10.3-2
- pull in some upstream fixes, particularly: imap folder acls (kollab#1816)

* Mon May 06 2013 Than Ngo <than@redhat.com> - 1:4.10.3-1
- 4.10.3

* Mon Apr 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.10.1-1
- 4.10.1

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:4.10.0-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:4.10.0-3
- Rebuild for Boost-1.53.0

* Fri Feb 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1:4.10.0-2
- pull in a few upstream patches

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Thu Nov 29 2012 Jan Grulich <jgrulich@redhat.com> - 1:4.9.3-3
- Rebuild (qjson)

* Fri Nov 23 2012 Dan Vratil <dvratil@redhat.com> - 1:4.9.3-2
- Rebuild against qjson 0.8.0

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 1:4.9.1-1
- 4.9.1

* Mon Aug 06 2012 Than Ngo <than@redhat.com> - 1:4.9.0-2
- add rhel/fedora condition

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 1:4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.97-1
- 4.8.97

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.95-2
- missing Kolab Resource (#835904)

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 1:4.8.95-1
- 4.8.95

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.90-2
- rebuild (shared-desktop-ontologies)

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.90-1
- 4.8.90

* Sun Jun 03 2012 Jaroslav Reznik <jreznik@redhat.com> - 1:4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.3-2
- s/kdebase-runtime/kde-runtime/

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 1:4.8.3-1
- 4.8.3

* Tue Apr 03 2012 Lukas Tinkl <ltinkl@redhat.com> 1:4.8.2-3
- 4.8.2 tarball respin

* Sun Apr 01 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.2-2
- KAlarmCal::EventAttribute::commandError makes Kontact crash (kde#297039)

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.2-1
- 4.8.2

* Mon Mar 12 2012 Jaroslav Reznik <jreznik@redhat.com> - 1:4.8.1-2
- fix version

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 1:4.8.1-1
- 4.8.1

* Wed Feb 08 2012 Rex Dieter <rdieter@fedoraproject.org> 1:4.8.0-2
- use akonadi_kcm_sqlite patch referenced on reviewboard instead

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 1:4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 1:4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 1:4.7.95-1
- 4.7.95
- drop fix linking wrt convenience lib nepomukfeederpluginlib patch

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.90-4
- fix Obsoletes: kdepim-runtime-devel versioning (missing epoch)

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.90-3
- drop useless -devel pkg

* Mon Dec 05 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:4.7.90-2
- move unversioned libnepomukdatamanagement-copy.so from -devel to -libs

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 1:4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.2-5.1
- rebuild against known working Qt headers for F16 final

* Thu Oct 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-5
- sqlite-support.patch, s/QSQLITE/QSQLITE3/

* Thu Oct 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-4
- disable akonadi nepomuk/strigi notification spam

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-3
- akonadi_maildispatcher_agent crashes when sending email (kde#283364)

* Sat Oct 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-2
- Kmail has duplicated folders after migration from previous version (kde#283467)

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-4
- pkgconfig-style deps

* Wed Sep 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.7.1-3
- upstream Ignore-items-with-empty-remote-ids-here patch 

* Tue Sep 20 2011 Radek Novacek <rnovacek@redhat.com> 1:4.7.1-2
- Enable SQLite support in akonadi

* Fri Sep 02 2011 Than Ngo <than@redhat.com> - 1:4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.7.0-1
- 4.7.0

* Mon Jul 11 2011 Jaroslav Reznik <jreznik@redhat.com> 1:4.6.95-1
- 4.6.95 (rc2)

* Thu Jun 30 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.6.90-1
- 4.6.90

* Fri Jun 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1:4.6.0-1
- 4.6.0
