Summary:	The NIS (Network Information Service) server
Url:		http://www.linux-nis.org/
Name:		ypserv
Version:	2.29
Release:	1
License:	GPL
Group:		System/Servers

Source0:	http://www.linux-nis.org/download/ypserv/%{name}-%{version}.tar.bz2
Source1:	ypserv-ypserv.init
Source2:	ypserv-yppasswdd.init
Source3:	ypserv-ypxfrd.init
Patch0:		ypserv-2.10-makefile.patch
Patch1:		ypserv-2.29-tirpc.patch
Patch2: 	ypserv-2.11-path.patch
Patch3:		ypserv-2.29-automake-1.13.patch
Patch6:		ypserv-2.5-nfsnobody2.patch
Patch11:	ypserv-2.13-ypxfr-zeroresp.patch

BuildRequires:	mawk libgdbm-devel libopenslp-devel
Requires:	rpcbind mawk make
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%track
prog %name = {
	url = http://www.linux-nis.org/download/ypserv/
	version = %version
	regex = %name-(__VER__)\.tar\.bz2
}

%description
The Network Information Service (NIS) is a system which provides network
information (login names, passwords, home directories, group information)
to all of the machines on a network.  NIS can enable users to login on
any machine on the network, as long as the machine has the NIS client
programs running and the user's password is recorded in the NIS passwd
database.  NIS was formerly known as Sun Yellow Pages (YP).

This package provides the NIS server, which will need to be running on
your network.  NIS clients do not need to be running the server.

Install ypserv if you need an NIS server for your network.  You'll also
need to install the yp-tools and ypbind packages onto any NIS client
machines.

%prep
%setup -q
%patch0 -p1 -b .makefix
%patch1 -p1 -b .tirpc~
%patch2 -p0 -b .path
%patch3 -p1 -b .am13~
%patch6 -p1
%patch11 -p1

aclocal -I m4
automake
autoconf

%build
%serverbuild
cp etc/README etc/README.etc
%configure2_5x --enable-checkroot \
	   --enable-fqdn \
	   --enable-yppasswd \
	   --libexecdir=%{_libdir}/yp \
	   --mandir=%{_mandir}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

install -m644 etc/ypserv.conf -D %buildroot%{_sysconfdir}/ypserv.conf
install -m755 %{SOURCE1} -D %buildroot%{_initrddir}/ypserv
install -m755 %{SOURCE2} -D %buildroot%{_initrddir}/yppasswdd
install -m755 %{SOURCE3} -D %buildroot%{_initrddir}/ypxfrd

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %buildroot%{_initrddir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service ypserv
%_post_service yppasswdd
%_post_service ypxfrd

%preun
%_preun_service ypserv
%_preun_service yppasswdd
%_preun_service ypxfrd
 
%files
%defattr(-,root,root)
%doc README INSTALL ChangeLog TODO NEWS
%doc etc/ypserv.conf etc/securenets etc/README.etc
%config(noreplace) %{_sysconfdir}/ypserv.conf
%config(noreplace) /var/yp/*
%{_initrddir}/*
%dir %{_libdir}/yp
%attr(755, root, root) %{_libdir}/yp/*
%attr(755, root, root) %{_sbindir}/*
%{_mandir}/*/*
%{_includedir}/*/*




%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 2.22-3mdv2011.0
+ Revision: 671949
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.22-2mdv2011.0
+ Revision: 608274
- rebuild

* Mon Feb 08 2010 Olivier Thauvin <nanardon@mandriva.org> 2.22-1mdv2010.1
+ Revision: 501893
- 2.22
- 2.22

* Sat May 09 2009 Olivier Thauvin <nanardon@mandriva.org> 2.19-8mdv2010.0
+ Revision: 373789
- s/portmapper/rpcbind
- s/portmapper/rpcbind

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 2.19-7mdv2009.1
+ Revision: 317954
- rediffed some fuzzy patches

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.19-6mdv2008.1
+ Revision: 178769
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 2.19-5mdv2008.0
+ Revision: 43311
- rebuild with new serverbuild macro (-fstack-protector)

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 2.19-4mdv2008.0
+ Revision: 36220
- rebuild with correct optflags

  + Olivier Thauvin <nanardon@mandriva.org>
    - requires portmapper instead portmap


* Fri Jul 21 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 07/21/06 10:43:13 (41827)
- rebuild

* Fri Jul 21 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 07/21/06 10:38:51 (41822)
Import ypserv

* Sat Feb 11 2006 Olivier Thauvin <nanardon@mandriva.org> 2.19-1mdk
- 2.19

* Sun Jan 08 2006 Olivier Blin <oblin@mandriva.com> 2.17-3mdk
- add LSB comments in initscripts (Sources 1, 2, 3)
- fix requires post/preun
- use 755 perms for executables

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.17-2mdk
- Rebuild

* Sat Jul 16 2005 Olivier Thauvin <nanardon@mandriva.org> 2.17-1mdk
- 2.17
- remove patch{8,9}, no need anymore

* Tue Mar 22 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14-2mdk
- fix build with -fPIE

* Wed Nov 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.14-1mdk
- 2.14
- sync with fedora patches
- cosmetics

* Mon Jan 19 2004 Frederic Lepied <flepied@mandrakesoft.com> 2.11-1mdk
- 2.11: SLP support

* Wed Nov 05 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.10-1mdk
- 2.10

