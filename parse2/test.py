from ciscoconfparse2 import CiscoConfParse
import re

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
parse = CiscoConfParse('../KOa201CS1_2024-05-20.txt', syntax='ios')   
                      # syntac  ios/iosxr

#print("----------------------- hostname")
#hostname_line = parse.find_objects('^hostname')[0]
#hostname = hostname_line.split()[1]
#print(hostname)

print("----------------------- hostname")
hostname_line = parse.find_objects('^hostname')[0]
hostname = hostname_line.re_match_typed(r'^hostname\s+(\S+)', default='')
print(hostname)

T = True
F = False

if F:
   print("----------------------- all interface")
   for intf_obj in parse.find_parent_objects(['^interface' ]):
           intf_name = " ".join(intf_obj.split()[1:])
           print(f"{intf_name}")
   
if T:
   print("----------------------- all interface dict build")
   int_type_dict = {}
   for intf_obj in parse.find_parent_objects(['^interface' ]):
           int_name = intf_obj.re_match_iter_typed("interface\s+(\S.*)")
           m = re.match(r'([a-zA-Z\-]+)([0-9\/]+)', int_name)
           int_type = m.groups()[0]
           if int_type in int_type_dict:
               int_type_dict[int_type] += 1
           else:
               int_type_dict[int_type] = 1
   
   int_dict = {}
   for k in int_type_dict:
      #print(f"{k} : {int_type_dict[k]}")
      int_dict[k] = {}

   for k in int_dict:
      print(f"{k} : {int_dict[k]}")

   for intf_obj in parse.find_parent_objects(['^interface' ]):
           int_name = intf_obj.re_match_iter_typed("interface\s+(\S.*)")
           m = re.match(r'([a-zA-Z\-]+)([0-9\/]+)', int_name)
           int_type = m.groups()[0]
           int_no = m.groups()[1]
           int_dict[int_type][int_no] = intf_obj

   for k in int_dict:
       for n in int_dict[k]:
           print(f"{k} -> {n} -> {int_dict[k][n].text}" )

   tmp = int_dict["Vlan"]["10"]
   print(tmp.text)
   for c in tmp.children:
       print(c.text)

if F:
   print("----------------------- Port-channel interface")
   for intf_obj in parse.find_parent_objects(['^interface Port-channel' ]):
           intf_name = " ".join(intf_obj.split()[1:])
           #number = intf_obj.re_match_iter_typed("Port-channel(\d.*)")
           number = intf_obj.re_match("Port-channel(\d.*)")
           print(f"{intf_name}",  number)

if F:
   print("----------------------- Vlan interface")
   for intf_obj in parse.find_parent_objects(['^interface Vlan' ]):
           intf_name = " ".join(intf_obj.split()[1:])
           #number = intf_obj.re_match_iter_typed("Port-channel(\d.*)")
           number = intf_obj.re_match("Vlan(\d.*)")
           print(f"{intf_name}",  number)
if F:
   print("----------------------- shutdown interface")
   for intf_obj in parse.find_parent_objects(['interface', 'shutdown']):
           intf_name = " ".join(intf_obj.split()[1:])
           print(f"Shutdown: {intf_name}")
if F:
   print("----------------------- interface trunk")
   for intf_obj in parse.find_parent_objects(['interface', 'switchport mode trunk']):
           intf_name = " ".join(intf_obj.split()[1:])
           description = intf_obj.re_match_iter_typed("description\s+(\S.*)").replace(",", "_")
           allow_trunk = intf_obj.re_match_iter_typed("switchport trunk allowed vlan\s+([1-9]\S.*)")
           add_allow_trunks = intf_obj.re_list_iter_typed("switchport trunk allowed vlan add\s+(\S.*)")
           channel_group = intf_obj.re_match_iter_typed("channel-group\s+(\S.*)")
           print(f"switchport mode trunk: {intf_name} {description}")
           print(f"                                     {allow_trunk}"  )
           if  len(add_allow_trunks) > 0:
              print(f"                                     {add_allow_trunks}"  )
           if  len(channel_group) > 0:
               print(f"                             channel_group: [{channel_group}]"  )
           #print(f"                             channel_group:[{channel_group}]"  )
   
if F:
   print("----------------------- interface access")
   for intf_obj in parse.find_parent_objects(['interface', 'switchport mode access']):
           intf_name = " ".join(intf_obj.split()[1:])
           description = intf_obj.re_match_iter_typed("description\s+(\S.*)").replace(",", "_")
           vlanid      = intf_obj.re_match_iter_typed("switchport access vlan\s+(\S.*)")

           print(f"switchport mode access: {intf_name}  {description}"  )
           print(f"                                     {vlanid}"  )

if F:
   print("----------------------- ip assignment interface ")
   for intf_obj in parse.find_parent_objects(['interface', 'ip address']):
           intf_name = " ".join(intf_obj.split()[1:])
           description = intf_obj.re_match_iter_typed("description\s+(\S.*)").replace(",", "_")
           ip_address  = intf_obj.re_match_iter_typed("ip address\s+(\S.*)")

           print(f"ip interface: {intf_name}  {description}"  )
           print(f"                                     {ip_address}"  )


if F:
   print("----------------------- vrf")
   for intf_obj in parse.find_parent_objects(['^ip vrf' ]):
           vrf_name = " ".join(intf_obj.split()[2:])
           rd  = intf_obj.re_match_iter_typed("rd\s+(\S.*)")
           print(f"{vrf_name} {rd}" )

if F:
   print("----------------------- vlan")
   for intf_obj in parse.find_parent_objects(['^vlan' ]):
           vlans  = intf_obj.re_match_iter_typed("vlan\s+(\S.*)").split(',')
           print(vlans)

if F:
   print("----------------------- ip route vrf")
   for intf_obj in parse.find_parent_objects(['^ip route vrf' ]):
           vrf_route  = intf_obj.re_match_iter_typed("ip route vrf\s+(\S.*)")
           print(vrf_route)

if F:
   print("----------------------- ip route")
   for intf_obj in parse.find_parent_objects(['^ip route\s+[1-9]' ]):
           route  = intf_obj.re_match_iter_typed("ip route\s+(\S.*)")
           print(route)

if F:
   print("----------------------- router")
   for intf_obj in parse.find_parent_objects(['^router' ]):
           router  = intf_obj.re_match_iter_typed("router\s+(\S.*)")
           print(router)

if F:
   print("----------------------- router detail")
   for router_obj in parse.find_parent_objects(['^router' ]):
           router_id  = router_obj.re_match_iter_typed("router\s+(\S.*)")
           print(router_id)
           address_familys = router_obj.re_list_iter_typed("address-family\s+(\S.*)")
           print(address_familys)

if F:
   print("----------------------- router detail2")
   for router_obj in parse.find_parent_objects(['^router' ]):
           router_id  = router_obj.re_match_iter_typed("router\s+(\S.*)")
           print(router_id)
           address_familys = router_obj.re_list_iter_typed("address-family\s+(\S.*)")
           print(address_familys)
           nbs = router_obj.re_list_iter_typed("neighbor\s+(\S.*)")
           print(nbs)

if F:
   print("----------------------- router detail3")
   for router_obj in parse.find_parent_objects(['^router' ]):
           router_id  = router_obj.re_match_iter_typed("router\s+(\S.*)")
           print(router_id)
           print("linenum:",router_obj.linenum)
           #print(router_obj.parent)
           #print(router_obj.children)
           for child_obj in router_obj.children:
              address_familys = child_obj.re_list_iter_typed("address-family\s+(\S.*)")
              if len(address_familys) > 0:
                  print("  ",address_familys)
                  for child2_obj in child_obj.children:
                     neighbor = child2_obj.re_list_iter_typed("neighbor\s+(\S.*)")
                     if len(neighbor) > 0:
                        #print(neighbor, child2_obj.parent.text)
                        print("        ",neighbor )


if F:
   for intf_obj in parse.find_objects(['^interface' ]):
           ips = intf_obj.re_list_iter_typed("ip address (\S.*)")
           print(f"{ips}")
   
if F:
   for intf_obj in parse.find_parent_objects(['^ip vrf' ]):
           intf_name = " ".join(intf_obj.split()[1:])
           print(f"{intf_name}")
   

if F:
   print("************************** test exec")
   names = ['aaa', 'bbbb', 'ccccc']
   
   for name in names:
       x = len(name)
       exec('{} = {}'.format(name, x))
   
   print(aaa) # 3
   print(bbbb) # 4
   print(ccccc) # 5
