%define	name	ypserv
%define	version	2.22
%define	release	%mkrel 1

Summary:	The NIS (Network Information Service) server
Url:		http://www.linux-nis.org/
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers

Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2
Source1:	ypserv-ypserv.init
Source2:	ypserv-yppasswdd.init
Source3:	ypserv-ypxfrd.init
Source4:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/%{name}-%{version}.tar.bz2.sign
Patch0:		ypserv-2.10-makefile.patch
Patch2: 	ypserv-2.11-path.patch
Patch6:		ypserv-2.5-nfsnobody2.patch
Patch11:	ypserv-2.13-ypxfr-zeroresp.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	mawk libgdbm-devel libopenslp-devel
Requires:	rpcbind mawk make
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

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
%patch2 -p0 -b .path
%patch6 -p1
%patch11 -p1

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
%makeinstall libexecdir=$RPM_BUILD_ROOT%{_libdir}/yp

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


