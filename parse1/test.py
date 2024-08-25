from ciscoconfparse2 import CiscoConfParse

##############################################################################
# Find all Cisco IOS interface names that are shutdown
##############################################################################
#
# Search for:
#     !
#     interface Foo
#      description ignore-this-line
#      shutdown
#     !

# Search a configuration in the test fixutres directory
#parse = CiscoConfParse('../KOa203FS1_2024-05-20.txt', syntax='ios')
parse = CiscoConfParse('../KOa201CS1_2024-05-20.txt', syntax='ios')   # syntac  ios/iosxr
# Find a parent line containing 'interface' and child line with 'shutdown'
hostname = parse.find_objects('hostname')[0]
print(hostname.text)
print(hostname.split())

#for intf_obj in parse.find_parent_objects(['interface', 'shutdown']):
for intf_obj in parse.find_parent_objects(['^interface' ]):
        intf_name = " ".join(intf_obj.split()[1:])
        print(f"{intf_name}")

for intf_obj in parse.find_objects(['^interface' ]):
        ip = intf_obj.re_list_iter_typed("ip address (\S.*)")
        print(f"{ip}")

for intf_obj in parse.find_parent_objects(['^ip vrf' ]):
        intf_name = " ".join(intf_obj.split()[1:])
        print(f"{intf_name}")

