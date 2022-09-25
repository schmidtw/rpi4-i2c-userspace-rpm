%global i2c_group i2c

Name:          rpi4-i2c-userspace
Version:       1.0.0
Release:       1%{?dist}
Summary:       Configure a RPI4 i2c for userspace use.
License:       Apache-2.0
BugURL:        https://github.com/schmidtw/rpi4-i2c-userspace-rpm
URL:           https://github.com/schmidtw/rpi4-i2c-userspace-rpm
BuildArch:     noarch

Requires(pre):  shadow-utils
Requires(pre):  glibc-common
Requires:       systemd-rpm-macros
Requires(post): systemd-udev

%description
Configure a RPI4 i2c for userspace use.

%package i2c0
Summary:    Enable and configure i2c0 as a userspace i2c interface.
BuildArch:  noarch
Requires:   rpi4-i2c-userspace

%description i2c0
Configure the i2c0 port to be on.

%package i2c1
Summary:    Enable and configure i2c1 as a userspace i2c interface.
BuildArch:  noarch
Requires:   rpi4-i2c-userspace

%description i2c1
Configure the i2c1 port to be on.

%prep
%setup -c -T

%build
# Create the module file.
echo "i2c-dev" > i2c.conf 

# Create the udev rule file.
echo 'KERNEL=="i2c-[0-9]*", GROUP="%{i2c_group}"' > 10-i2c_group.rules

%pre
getent group %{i2c_group} > /dev/null || %{_sbindir}/groupadd -r %{i2c_group}

%install
%{__install} -p -Dm0644 i2c.conf            %{buildroot}%{_modulesloaddir}/i2c.conf 
%{__install} -p -Dm0644 10-i2c_group.rules  %{buildroot}%{_udevrulesdir}/10-i2c_group.rules

%post
# Only write when this is installed.
if [ $1 -eq 1 ] ; then
    # Enable i2c
    echo ""                                             >> /boot/config.txt
    echo "# Start managed by rpi4-i2c-userspace rpm"    >> /boot/config.txt
    echo "dtparam=i2c_arm=on"                           >> /boot/config.txt
    echo "i2c-bcm2708"                                  >> /boot/config.txt
    echo "# End managed by rpi4-i2c-userspace rpm"      >> /boot/config.txt
fi


%post i2c0
# Only write when this is installed.
if [ $1 -eq 1 ] ; then
    echo ""                                                 >> /boot/config.txt
    echo "# Start managed by rpi4-i2c-userspace-i2c0 rpm"   >> /boot/config.txt
    echo "dtparam=i2c0=on"                                  >> /boot/config.txt
    echo "# End managed by rpi4-i2c-userspace-i2c0 rpm"     >> /boot/config.txt
fi

%post i2c1
# Only write when this is installed.
if [ $1 -eq 1 ] ; then
    echo ""                                                 >> /boot/config.txt
    echo "# Start managed by rpi4-i2c-userspace-i2c1 rpm"   >> /boot/config.txt
    echo "dtparam=i2c1=on"                                  >> /boot/config.txt
    echo "# End managed by rpi4-i2c-userspace-i2c1 rpm"     >> /boot/config.txt
fi

%postun
# Only run when uninstalled
if [ $1 -eq 0 ] ; then
    sed -i '/^# Start managed by rpi4-i2c-userspace rpm/,/^# End managed by rpi4-i2c-userspace rpm/d' /boot/config.txt
fi

%postun i2c0
# Only run when uninstalled
if [ $1 -eq 0 ] ; then
    sed -i '/^# Start managed by rpi4-i2c-userspace-i2c0 rpm/,/^# End managed by rpi4-i2c-userspace-i2c0 rpm/d' /boot/config.txt
fi

%postun i2c1
# Only run when uninstalled
if [ $1 -eq 0 ] ; then
    sed -i '/^# Start managed by rpi4-i2c-userspace-i2c1 rpm/,/^# End managed by rpi4-i2c-userspace-i2c1 rpm/d' /boot/config.txt
fi


%files
%defattr(-,root,root)
%{_modulesloaddir}/i2c.conf 
%{_udevrulesdir}/10-i2c_group.rules

%files i2c0
# none

%files i2c1
# none

%changelog
* Sat Sep 24 2022 Weston Schmidt <weston_schmidt@alumni.purdue.edu> - 1.0.0-1
- Initial release

