%define __noautoreq '.*/bin/awk|.*/bin/gawk'

Summary:	The NIS (Network Information Service) server
Name:		ypserv
Version:	2.32
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		https://www.linux-nis.org/
Source0:	http://www.linux-nis.org/download/ypserv/%{name}-%{version}.tar.gz
Source1:	ypserv.service
Source2:	yppasswdd.service
Source3:	ypxfrd.service
Patch0:		ypserv-2.10-makefile.patch
#Patch1:		ypserv-2.29-tirpc.patch
Patch2:		ypserv-2.11-path.patch
Patch3:		ypserv-2.29-automake-1.13.patch
Patch6:		ypserv-2.5-nfsnobody2.patch
Patch11:	ypserv-2.13-ypxfr-zeroresp.patch
BuildRequires:	mawk
BuildRequires:	gdbm-devel
BuildRequires:	openslp-devel
BuildRequires:	pkgconfig(libtirpc)
Requires:	make
Requires:	mawk
Requires:	rpcbind
Requires(post,preun):	rpm-helper

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

%files
%doc README INSTALL ChangeLog TODO NEWS
%doc etc/ypserv.conf etc/securenets etc/README.etc
%config(noreplace) %{_sysconfdir}/ypserv.conf
%config(noreplace) /var/yp/*
%{_unitdir}/*
%dir %{_libdir}/yp
%attr(755, root, root) %{_libdir}/yp/*
%attr(755, root, root) %{_sbindir}/*
%{_mandir}/*/*
%{_includedir}/*/*

%post
%_post_service ypserv
%_post_service yppasswdd
%_post_service ypxfrd

%preun
%_preun_service ypserv
%_preun_service yppasswdd
%_preun_service ypxfrd

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1
autoreconf -fi

%build
%serverbuild
cp etc/README etc/README.etc
%configure2_5x \
	--enable-checkroot \
	--enable-fqdn \
	--enable-yppasswd \
	--libexecdir=%{_libdir}/yp \
	--mandir=%{_mandir}
%make_build

%install
%make_install

install -m644 etc/ypserv.conf -D %{buildroot}%{_sysconfdir}/ypserv.conf
mkdir -p %{buildroot}%{_unitdir}
install -m755 %{SOURCE1} -D %{buildroot}%{_unitdir}/ypserv
install -m755 %{SOURCE2} -D %{buildroot}%{_unitdir}/yppasswdd
install -m755 %{SOURCE3} -D %{buildroot}%{_unitdir}/ypxfrd
