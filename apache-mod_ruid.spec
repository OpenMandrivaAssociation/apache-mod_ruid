#Module-Specific definitions
%define mod_name mod_ruid
%define mod_conf A89_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Suexec module for apache 2.x, based on mod_suid2
Name:		apache-%{mod_name}
Version:	0.6
Release:	%mkrel 13
Group:		System/Servers
License:	Apache License
URL:		http://websupport.sk/~stanojr/projects/mod_ruid/
Source0:	http://websupport.sk/~stanojr/projects/mod_ruid/mod_ruid-%{version}.tar.gz
Source1:	README.%{mod_name}
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	libcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod_ruid is suexec module for apache 2.0, based on mod_suid2.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} .
cp %{SOURCE2} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c -Wl,-lcap %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.%{mod_name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
