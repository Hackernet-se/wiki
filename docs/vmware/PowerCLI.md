---
title: PowerCLI
permalink: /PowerCLI/
---

[Category:VMware](/Category:VMware "wikilink") PowerCLI är ett Windows
Powershell-gränssnitt för hantering av VMware vSphere. PowerCLI
distribueras som en Powershell snapin, och innehåller över 370
Powershell-cmdlets för att hantera och automatisera vSphere och vCloud.

"a powerful command-line tool that lets you automate all aspects of
vSphere management, including network, storage, VM, guest OS and more" -
VMware

Installation
------------

Ladda ner installationsfilen från VMwares hemsida alternativt importera
det från online repo.

``` powershell
Install-Module -Name VMware.PowerCLI
Get-PowerCLIVersion
```

Anslut till din ESXi/vCenter med:

`Connect-VIServer`

Untrusted certificate

`Set-PowerCLIConfiguration -InvalidCertificateAction ignore -confirm:$false`

Exempel
-------

Flytta alla vms från en datastore till en annan.

`Get-Datastore`
`Get-VM -Datastore Datastore1 | Move-VM -Datastore Datastore2 -DiskStorageFormat thin`

Flytta alla vms från en host till en annan.

`Get-VMHost 172.20.0.2 | Get-VM | Move-VM -destination 172.20.0.8`

Visa alla **notes**

`Get-VM | Select-Object -ExpandProperty Notes`

Lista **hardware version** för alla vms

`Get-VM | Select Name, Version`

Ladda upp fil till datastore

`Copy-DatastoreItem -Item linux.iso -Destination vmstore:\DC\DATASTORE\linux.iso`

Hitta vilken vm som har en viss **MAC-adress**

``` powershell
Get-vm | Select Name, @{N=“Network“;E={$_ | Get-networkAdapter | ? {$_.macaddress -eq “00:50:56:00:50:43“}}} |Where {$_.Network-ne “”}
```

Kolla **NTP** för hostarna

``` powershell
Get-VMHost | Sort-Object Name | Select-Object Name, @{N=”Cluster”;E={$_ | Get-Cluster}}, @{N=”Datacenter”;E={$_ | Get-Datacenter}}, @{N=“NTPServiceRunning“;E={($_ | Get-VmHostService | Where-Object {$_.key-eq “ntpd“}).Running}}, @{N=“StartupPolicy“;E={($_ | Get-VmHostService | Where-Object {$_.key-eq “ntpd“}).Policy}}, @{N=“NTPServers“;E={$_ | Get-VMHostNtpServer}}, @{N="Date&Time";E={(get-view $_.ExtensionData.configManager.DateTimeSystem).QueryDateTime()}} | format-table -autosize
Get-VMHost | Get-VmHostService | Where-Object {$_.key -eq "ntpd"} | Set-VMHostService -policy "on"; Get-VMHost | Add-VMHostNtpServer -NtpServer 0.se.pool.ntp.org; Get-VMHost | Get-VMHostFirewallException | Where-Object {$_.Name -eq "NTP client"} | Set-VMHostFirewallException -Enabled:$true; Get-VMHost | Get-VmHostService | Where-Object {$_.key -eq "ntpd"} | Start-VMHostService
```

Lista CPUer

``` powershell
Get-VMHost | Sort Name | Get-View | Select Name, @{N=“CPU“;E={$_.Hardware.CpuPkg[0].Description}}
```

Byt från e1000 till vmxnet3

``` powershell
Get-VM -name "<VM>" | Get-NetworkAdapter | Where { $_.Type -eq "E1000"} | Set-NetworkAdapter -Type "vmxnet3"
```

Byt till multipathing på lun större än 1TB

``` powershell
Get-VMHost | Get-ScsiLun -LunType disk | Where {$_.MultipathPolicy -notlike "RoundRobin"} | Where {$_.CapacityGB -ge 1000} | Set-Scsilun -MultiPathPolicy RoundRobin
```

**VLAN**-hantering om man inte kör vDS. Create and delete.

``` powershell
Get-Datacenter -Name DC01 | Get-VMHost | Get-VirtualSwitch -name vSwitch1 | new-VirtualPortGroup -name "DMZ01" -vlanid 101

Get-Datacenter -Name DC01 | Get-VMHost | Get-VirtualSwitch -Name vSwitch1 | Get-VirtualPortGroup -Name "DMZ01" | Remove-VirtualPortGroup
```

Sätta **Syslogserver**

``` powershell
Get-VMHost | Get-VMHostSysLogServer
Get-Cluster cluster | Get-VMHost | Get-AdvancedSetting -Name Syslog.global.logHost | Set-AdvancedSetting -value "syslog.hackernet.se" -Confirm:$False
```

Lagra logg på persistant storage

`Get-Cluster cluster | Get-VMhost | Get-AdvancedSetting -Name Syslog.global.logDirUnique | Set-AdvancedSetting -Value $True -Confirm:$False`
`Get-Cluster cluster | Get-VMHost | Get-AdvancedSetting -Name Syslog.global.logDir | Set-AdvancedSetting -value "[datastore] esxi_logs" -Confirm:$False`

**DNS**

``` powershell
Get-VMHost | Select Name, @{N='DNS Server(s)';E={$_.Extensiondata.Config.Network.DnsConfig.Address -join ', '}} | FT -autosize
Get-VMHost | Get-VMHostNetwork -ErrorAction SilentlyContinue | Set-VMHostNetwork -DnsAddress @("10.240.100.81", "10.60.0.81")
```

Find **Thick** VM disks

``` powershell
 Get-Datastore | Get-VM | Get-HardDisk | Where {$_.storageformat -eq "Thick" } | Select Parent, Name, CapacityGB, storageformat | FT -AutoSize
```

Script
------

Ett script för att skapa vm. New-VM.ps1

``` powershell
#List functions first

function Gather-Info {
[string]$script:VMName = Read-host "Enter the name of the VM you wish to create"
Get-VMHost | Format-Wide
[string]$script:HOSTName = Read-host "Enter host"
Get-Datastore -VMHost $HOSTName | Format-Wide
[string]$script:DSName = Read-Host "Enter datastore"
[string]$script:VERSION = Read-Host "Enter VM-Version, exempel v9"
[int]$script:NUMCPU =  Read-Host "Antal CPU-cores"
[int]$script:MEMORYMB =  Read-Host "RAM, Antal MB"
[int]$script:DiskGB =  Read-Host "Disk, Antal GB"
Get-VirtualPortGroup -VMHost $HOSTName
[string]$script:NETWORK = Read-Host "Select Network"
[string]$script:NOTES = Read-Host "Notes"
[System.Enum]::GetNames([VMware.Vim.VirtualMachineGuestOsIdentifier]) | Format-Wide
[string]$script:GUESTID =  Read-Host "Select that guestid"
}


function CreateVM {
Write-Host -ForegroundColor Green "Now the magic happens"
Write-Host "Creating VM"
New-VM -Name $VMName -VMHost $HOSTName -Datastore $DSName -DiskStorageFormat Thin -version $VERSION -GuestId $GUESTID -NumCpu $NUMCPU -MemoryMB $MEMORYMB -Notes $NOTES -DiskGB $DiskGB -NetworkName $NETWORK | out-null
Write-Host -ForegroundColor Green "Convert to vmxnet3?"
Get-VM $VMName | Get-NetworkAdapter | Set-NetworkAdapter -Type vmxnet3 | out-null
Start-Sleep -Seconds 1;
Write-Host "Starting the VM"
Start-vm -VM $VMName -runAsync
Start-Sleep -Seconds 1;
Write-Host -ForegroundColor Green "Power On Complete"
}


#Connect to vSphere
$VSPHERE = Read-host "Skriv IP till vCenter eller ESXi-host, tryck enter"
Connect-VIServer $VSPHERE


#Use functions and verify input
Do {
Gather-Info
Write-Host $VMName, $HOSTName, $DSName, HW $VERSION, $NUMCPU,vCPU $MEMORYMB,MB RAM $DiskGB,GB $NETWORK, $GUESTID, $NOTES
$confirmation = Read-Host "Proceed y/n"
}
until ($confirmation -eq 'y')

CreateVM
break
```

Script för att kolla disktyp. Disktype.ps1

``` powershell
Connect-viserver "VCENTER_NAME"  #ange namn på Vcenter

$report = @()

foreach ($vm in Get-VM ){
$vmhdd = $vm | Get-HardDisk
foreach ($vmdisk in $vmhdd){
  $diskStyle = $null
  $format = $vmdisk.StorageFormat

$list = '' | select Name,Cluster,VMDK,DiskMode,DiskFormat,Filename
$list.Name = $vm.Name
$list.Cluster = $vm.VMHost.Parent
$list.VMDK = $vmdisk.name
$list.DiskMode = $vmdisk.Persistence
$list.DiskFormat = $vmdisk.StorageFormat
$list.Filename = $vmdisk.filename

$report += $list
}}
$report | Sort Name | Export-Csv -NoTypeInformation -Path C:\temp\vm_disk_type.csv   #Här sätter du vart du vill spara filen, nu sparas den under C:\temp
```