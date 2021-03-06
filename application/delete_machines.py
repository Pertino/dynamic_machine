#!/usr/bin/python3
'''
Created on Jun 14, 2014

@author: lwoydziak
'''
from jsonconfigfile import Env
from providers import digitalOceanHosting
from dynamic_machine.machine import Machine
from dynamic_machine.inventory import Inventory

def destroyNodes(filter):
    onDigitalOcean = digitalOceanHosting()
    name = Env().get("BaseHostName")
    machines = []
    
    # split
    for item in Inventory(onDigitalOcean).list(filteredByHost=name):
        if filter and not filter in item.name:
            continue 
        machine = Machine(onDigitalOcean, existing=True).name(item.name)
        machine.destroy()
        machines.append(machine)
    
    #join
    for machine in machines:
        machine.waitUntilDestroyed()    
    
def DestroyMachines(filter):
    initialJson = '{ \
        "DigitalOcean" : { \
            "Client ID"     : "None", \
            "API Key"       : "None", \
            "location"      : "None", \
            "image"         : "None", \
            "size"          : "None" \
        },\
        "BaseHostName": "None"\
    }'
    Env(initialJson, ".dynamicMachine", "DYNAMIC_MACHINE_CONFIG")
    destroyNodes(filter)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Delete Machines.')
    parser.add_argument('--filter', help='The filename of the JSON file containing the list of commands.',required=False)
    args = parser.parse_args()
    try:
        DestroyMachines(args.filter)
        exit(0)
    except Exception as e:
        print (str(e))
        exit(1)