@set year=%date:~0,4%
@set month=%date:~5,2%
@set day=%date:~8,2%
@set h=%time:~0,2%
@if /i %h% LSS 10 (set h=0%time:~1,1%)
@set m=%time:~3,2%
@set s=%time:~6,2%

@set param_time=%year%%month%%day%_%h%%m%%s%

vfctrl_usb.exe printall > param_list_%param_time%.txt
