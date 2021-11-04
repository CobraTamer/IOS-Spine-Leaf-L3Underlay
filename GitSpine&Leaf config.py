#By Taha Yusuf
#AUtomation of a layer 3 spine and leaf topology using Etherchannel for Maximum bandwidth on uplinks between spine and leaf
#Based on the Netmiko SSH module, this works on all IOS 12-15 
#Utilising ROUTED PORTS, OSPF, ECMP.
#Very scalable. You can add new leafs by simply adding it to the YAML file, if you need to add spines again this can be accomplished by adding to the YAML config file.
#If there are no port available on the spines, in order to add a new leaf, you can use any Stacking technology VPC,VSS,Stackwise etc for more ports by stacking the spines
# and the same can also be done for the leafs.

#Importing Yaml module, Yaml error for error handeling, Yaml Loader for yaml key:value to python  dictionary and the one and only 'NetMiko' SSH connection handler from the netmiko module

import yaml
from yaml.error import YAMLError
from yaml.loader import SafeLoader
from netmiko import ConnectHandler



with open ('Spine and Leaf fabricALL.yml') as f:
    try:
        data = yaml.load(f, Loader=SafeLoader)
        keys = list(data.keys())
        Values = list(data.values())       
        
            #Nested loop through the YAML file for the configuration. 
            #At moment no error checking or any form of imperative functions just declartive to parse information to NetMiko Module
            #The purpose of this code was to build the LAB Spine and leaf underlay ASAP.
            #In order to reuse the code you can simply edit the YAML file e.g you can add further leafs or spines or change 
            # layer 3 addressing or even LACP port channel memebers

        for device in keys:
            for VARinterfaces in data[device]['Interfaces']:
                #This was just a test I like to print out the variables to visually inspect the out put
                #However this also provides a feedback on the declaratve automation process
                print("===================="+"On-boarding Device" + device +"===========================")
                print("Device Name: " + device)
                print("device Management IP: " +  data[device]['HostIPv4Address'])
                print("Interface" + VARinterfaces)
                print(data[device]['Interfaces'][VARinterfaces]['InterfaceRange'])
                print(data[device]['Interfaces'][VARinterfaces]['channelgroup'])
                print(data[device]['Dynamic Routing']['OSPF1']['ECMPmaximum-Paths'])

                
                #created variables to store YAML configuration(see YAML file)  
                InterfaceRange = data[device]['Interfaces'][VARinterfaces]['InterfaceRange']
                PortChannelGroup =  data[device]['Interfaces'][VARinterfaces]['channelgroup']
                IntDescription = data[device]['Interfaces'][VARinterfaces]['Description1']
                IntIPv4addresses = data[device]['Interfaces'][VARinterfaces]['IPV4Address']
                IntNetMask = data[device]['Interfaces'][VARinterfaces]['Netmask']
                intOSPFP = data[device]['Dynamic Routing']['OSPF1']['OSPFprocessID']
                intECMP = data[device]['Dynamic Routing']['OSPF1']['ECMPmaximum-Paths']
                ManIP =  data[device]['HostIPv4Address']
                print(IntDescription)
                print(IntIPv4addresses)
                print(IntNetMask)
                print(intOSPFP)
                #The netmiko connection fucntion
                cisco_device = {
                    'device_type': 'cisco_ios',
                    'host':   ManIP,
                    'username': #'username',
                    'password': #'password',
                    'port' : 22,          # defaults SSH port 22
                    'secret': #'enable passoword',     # 
                }
                net_connect = ConnectHandler(**cisco_device)

                net_connect.enable()

               #Parsing the variables and the IOS commands into a variable called "commands"
                commands =['interface range ' + InterfaceRange ,
                'No switchport' , 'channel-protocol lacp' , 
                'channel-group ' + PortChannelGroup + ' mode active' ,
                'description ' + IntDescription, 
                'int port-channel ' + PortChannelGroup, 
                'description '+ IntDescription, 
                'IP address ' + IntIPv4addresses +" "+ IntNetMask, 
                'Router OSPF '+ intOSPFP, 
                'maximum-paths '+ intECMP ]

              
               #Sending the configuration + the cli commands to the Layer 3 swicthes.
               
          
                result = net_connect.send_config_set(commands)
               
  
        
                print(result)

                
  
        
               
    
    except yaml.YAMLError as ErrorMsg:
                print(ErrorMsg)
