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
parse = CiscoConfParse('../KOa203FS1_2024-05-20.txt', syntax='ios')

# Find a parent line containing 'interface' and child line with 'shutdown'
for intf_obj in parse.find_parent_objects(['interface', 'shutdown']):
        intf_name = " ".join(intf_obj.split()[1:])
        print(f"Shutdown: {intf_name}")

