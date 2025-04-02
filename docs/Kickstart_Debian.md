---
title: Kickstart Debian
permalink: /Kickstart_Debian/
---

Unattended
----------

Bootparameter

`append vga=normal initrd=os/debian7/initrd.gz preseed/url=`[`http://`](http://)<url>`/Debian.conf interface=auto priority=critical auto=true`

`####################################################################`
`#  PRESEED - Created Wed Apr  1 13:18:08 2015`
`####################################################################`

`# Wiki: `[`http://wiki.debian.org/DebianInstaller/Preseed`](http://wiki.debian.org/DebianInstaller/Preseed)
`# Great work!  Thanks for preseed and the d-i installer`


`####################################################################`
`# Installation Sources`
`####################################################################`

`# Where are we pulling bits from?`
`#`
`# Note:  To use your own local repository, this is what you want`
`# to edit.`
`#`
`# It should look like this:`
`#d-i     mirror/http/hostname    string (IP Address of your local server)`
`#d-i     mirror/http/directory   string (HTTP Path to your Repository - like /natty )`

`d-i     mirror/http/hostname    string ftp.se.debian.org`
`d-i     mirror/http/directory   string /debian/`
`d-i     mirror/suite            string `

`# Post install APT setup`
`d-i     apt-setup/uri_type      select d-i`
`d-i     apt-setup/hostname      string ftp.se.debian.org`
`d-i     apt-setup/directory     string /debian/`
`d-i     apt-setup/another       boolean false`
`d-i     apt-setup/security-updates      boolean false`
`d-i     finish-install/reboot_in_progress note`
`d-i     prebaseconfig/reboot_in_progress        note`

`d-i     apt-setup/non-free     boolean true`
`d-i     apt-setup/contrib  boolean true`

`####################################################################`
`# Networking`
`####################################################################`

`# Network Configuration`

`d-i     netcfg/get_hostname     string unassigned-hostname`
`d-i    netcfg/get_hostname     seen true `
`d-i     netcfg/get_domain       string unassigned-domain`
`d-i    netcfg/get_domain   seen true  `
`d-i     netcfg/disable_dhcp     boolean false`
`d-i    mirror/http/proxy   string  `
`d-i     netcfg/choose_interface select eth0`
`d-i     netcfg/wireless_wep     string`

`####################################################################`
`# Disk Partitioning/Boot loader`
`####################################################################`

`d-i     partman-auto/disk               string /dev/sda`
`d-i     partman-auto/method             string regular`
`d-i    partman-auto/choose_recipe  select atomic`


`# This makes partman automatically partition without confirmation.`
`d-i     partman/confirm boolean true`
`d-i     partman-partitioning/confirm_write_new_label boolean true`
`d-i     partman/choose_partition select finish`
`d-i     partman/confirm_nooverwrite boolean true `
`d-i    partman/confirm_write_new_label boolean true`

`# This one makes grub-installer install to the MBR even if finds some other OS`
`# too, which is less safe as it might not be able to boot that other OS.`
`d-i     grub-installer/with_other_os    boolean true`

`####################################################################`
`# Localizations`
`####################################################################`

`# Install Time `
`d-i    console-tools/archs string skip-config`
`d-i    debian-installer/locale string en_US`
`d-i    console-keymaps-at/keymap select sv`

`d-i     languagechooser/language-name-fb    select English`
`d-i     debian-installer/locale             select en_US.UTF-8`

`# Timezone`
`d-i     tzconfig/gmt            boolean true`
`d-i     tzconfig/choose_country_zone/Europe select Stockholm`
`d-i     tzconfig/choose_country_zone_single boolean true`
`d-i    time/zone   select  Europe/Stockholm`
`d-i    clock-setup/utc boolean true`
`d-i    kbd-chooser/method  select  American English`
`d-i    mirror/country  string  manual`
`d-i     clock-setup/ntp boolean false`

`# X11 config`
`xserver-xorg     xserver-xorg/autodetect_monitor              boolean true`
`xserver-xorg     xserver-xorg/config/monitor/selection-method select medium`
`xserver-xorg     xserver-xorg/config/monitor/mode-list        select 1024x768 @ 60 Hz`
`xserver-xorg     xserver-xorg/config/display/modes            multiselect 1024x768, 800x600`

`####################################################################`
`# User Creation`
`####################################################################`

`# Root User`
`d-i    passwd/root-password-crypted    passwd   Pa$$w0rd`

`# Mortal User`
`d-i    passwd/user-fullname            string `
`d-i    passwd/username                 string hacker`
`d-i    passwd/user-password-crypted    passwd Pa$$w0rd`

`####################################################################`
`# Software Selections`
`####################################################################`

`popularity-contest popularity-contest/participate boolean false`

`tasksel    tasksel/first   multiselect standard`
`d-i    pkgsel/include  string   openssh-server open-vm-tools systemd-sysv`
`d-i    grub-installer/only_debian  boolean true`
`####################################################################`
`# Additional preseed entries (from data/debconf)`
`####################################################################`

`exim4-config exim4/no_config boolean true`

[Category:Kickstart](/Category:Kickstart "wikilink")