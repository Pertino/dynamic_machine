#!/usr/bin/python3
'''
Created on Jun 14, 2014

@author: lwoydziak
'''
from jsonconfigfile import Env
from providers import digitalOceanHosting
from dynamic_machine.machine import Machine

'''usage: 
create_machine.py | tee cm.txt                                                                                 # print to screen and save output 
cat cm.txt | awk '{match( $0, /\(.*\)/ ) ; s = substr($0,RSTART, RLENGTH); gsub(/[()]/, "", s); print s}'      # print new machine IP
rm cm.txt                                                                                                      # clean up
'''

def buildNode(hostname):
    onDigitalOcean = digitalOceanHosting()
    machine = Machine(onDigitalOcean).name(hostname)\
                                     .image(Env().get("DigitalOcean", "image"))\
                                     .location(Env().get("DigitalOcean", "location"))\
                                     .size(Env().get("DigitalOcean", "size"))\
                                     .sshKey(Env().get("DigitalOcean", "sshKey"))\
                                     .create()
    machine.waitUntilReady()

def CreateMachine():
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
    buildNode(Env().get("BaseHostName"))



if __name__ == '__main__':
    try:
        CreateMachine()
        exit(0)
    except Exception as e:
        print (str(e))
        exit(1)