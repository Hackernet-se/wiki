---
title: NFS
permalink: /NFS/
---

[Category:Guider](/Category:Guider "wikilink") Network File System (NFS)
är ett filsystem som tillåter datorer att komma åt filer över ett
nätverk på ungefär samma sätt som de kan komma åt filer på lokal
lagring. Detta är användbart för att dela filer mellan flera servrar.
Här följer generella inställningar för server och klient, de fungerar i
de flesta fall.

Installation
------------

### Server

`sudo apt-get update && sudo apt-get -y install nfs-kernel-server`

### Klient

`sudo apt-get update && sudo apt-get -y install nfs-common`

Konfiguration
-------------

### Server

`sudo mkdir /nfsroot`
`sudo sh -c 'echo "/nfsroot 192.168.1.16/30(rw,root_squash,subtree_check)" >> /etc/exports'`
`sudo exportfs -a`
`sudo service nfs-kernel-server start`

### Klient

`sudo mkdir /nfsroot`
`sudo sh -c 'echo "192.168.1.50:/nfsroot /nfsroot nfs rw,async,hard,intr 0 0" >> /etc/fstab'`
`sudo mount /nfsroot`

Options
-------

Ibland kan man behöva ändra egenskaperna för NFS-share:n. T.ex. om man
har problem med att program sätter lock på filer. Här tas de vanligaste
alternativen upp som är bra att känna till. Det mesta görs på
klientsidan.

**Klient**
**rw**: Read/write filesystem.
**ro**: Read-only filesystem. Remote NFS clients can’t modify the
filesystem.
**hard**: Applications using files stored on an NFS will always wait if
the server goes down. User cannot terminate the process unless the
option intr is set.
**soft**: Applications using files stored on an NFS will wait a
specified time (using the timeo option) if the server goes down, and
after that, will throw an error.
**intr**: Allows user interruption of processes waiting on a NFS
request.
**timeo=<num>**: For use with the soft option. Specify the timeout for
an NFS request.
**nolock**: Disable file locks. Useful with older NFS servers.
**noexec**: Disable execution of binaries or scripts on an NFS share.
**nosuid**: Prevents users from gaining ownership of files on the NFS
share.
**rsize=<num>**: Sets the read block data size. Defaults to 8192 on
NFSv2 and NFSv3, and 32768 on NFSv4.
**wsize=<num>**: Sets the write block data size. Defaults to 8192 on
NFSv2 and NFSv3, and 32768 on NFSv4.
**Server**
**rw**: Read/write filesystem.
**ro**: Force clients to connect in the read-only filesystem mode
only.
**no_root_squash**: The root account on the client machine will have
the same privilege level as the root on the server machine. This option
has security implications; do not use unless you are sure you need it.
**no_subtree_check**: Disable file location checks on partial volume
exports. This option will speed up transfers on full volume exports.
**sync**: Force all transfers to operate in synchronous mode, so all
clients will wait until their operations are really done. This can avoid
data corruption in the event of a server crash.