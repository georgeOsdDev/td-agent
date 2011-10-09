Summary: td-agent
Name: td-agent
Version: 1.0.10
License: APL2
Release: 0%{?dist}

Group: System Environment/Daemons
Vendor: Treasure Data, Inc.
URL: http://treasure-data.com/
Source: %{name}-%{version}.tar.gz
Source1: %{name}.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

Requires: /usr/sbin/useradd /usr/sbin/groupadd
Requires: /sbin/chkconfig
Requires: openssl readline
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(build): gcc gcc-c++ pkgconfig libtool openssl-devel readline-devel

# 2011/08/01 Kazuki Ohta <kazuki.ohta@gmail.com>
# prevent stripping the debug info.
%define debug_package %{nil}
%define __strip /bin/true

%description

%prep

%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
# cleanup first
rm -rf $RPM_BUILD_ROOT
# install programs
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
# install init.d script
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
install -m 755 %{S:1} $RPM_BUILD_ROOT/etc/init.d/%{name}
# create log dir
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "adding 'td-agent' group..."
getent group td-agent >/dev/null || /usr/sbin/groupadd -r td-agent
echo "adding 'td-agent' user..."
getent passwd td-agent >/dev/null || \
  /usr/sbin/useradd -r -g td-agent -d %{_localstatedir}/lib/td-agent -s /sbin/nologin -c 'td-agent' td-agent
chown -R td-agent:td-agent /var/log/%{name}
if [ ! -e "/etc/td-agent/td-agent.conf" ]; then
  echo "Installing default conffile $CONFFILE ..."
  cp -f /etc/td-agent/td-agent.conf.tmpl /etc/td-agent/td-agent.conf
fi
/sbin/chkconfig --add td-agent
/sbin/service td-agent start >/dev/null 2>&1 || :

%preun
if [ $1 = 0 ] ; then
  /sbin/service td-agent stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del td-agent
fi

%files
%defattr(-,root,root)
/usr
/etc/td-agent
/etc/init.d/td-agent
/var/log/td-agent

%changelog
* Mon Oct 01 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.10
- fix posinst

* Mon Oct 01 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.9
- fluent v0.9.16
- fluent-plugin-scribe v0.9.10

* Mon Sep 20 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.8
- fluent v0.9.14
- fluent-plugin-td v0.9.10

* Mon Sep 20 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.6
- fluent v0.9.13

* Mon Sep 16 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.5
- fluent v0.9.10
- fluent-plugin-scribe v0.9.8

* Mon Sep 05 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.4
- fluent v0.9.9
- add fluent-plugin-scribe gem

* Sun Aug 18 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.3
- fluent v0.9.8

* Sun Aug 07 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.2
- fix calling undefined function in daemon mode

* Sun Aug 07 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.1
- fluent v0.9.7, with fluent-plugin-td gem

* Mon Aug 01 2011 Kazuki Ohta <k@treasure-data.com> - 1.0.0
- fluent v0.9.5. initial packaging for Scientific Linux 6
