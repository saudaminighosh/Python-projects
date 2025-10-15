#!/usr/bin/python
# -*- coding: utf-8 -*-
#Developed by EASUOGH
#First Release of SMSF Health Check Script. Script is verified on ECCD 2.25 and compatible with SMSF 0.16.x and 0.17.x


import time
import os
import paramiko
import fileinput
from datetime import datetime

os.chdir('/home/eccd')
ip = input('Enter ip of master: ')
user = input('Enter username: ')
jk= input('Do you have password(y/n): ')
if jk=="y":
    pass1 = input('Enter password: ')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=pass1, look_for_keys=False, allow_agent=False)
else:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(ip, username=user, password=None)
current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
str_current_datetime = str(current_datetime)

ns = input('\nPlease provide namespace: ')
chan = ssh.invoke_shell()
time.sleep(2)
var = 'kubectl get nodes -o wide' + '\n'
chan.send(var)
time.sleep(2)
chan.send('kubectl get ns' + '\n')
time.sleep(2)
var = 'kubectl get SmsfMesh -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get IstioOperator -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get pods -o wide -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get pods -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'helm list -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
resp = chan.recv(999999999)
buff =""
buff += resp.decode('ascii')
filename = 'HC_' + str_current_datetime + '.log'
f = open(filename, 'w')
f.write(buff)
print(buff)
f = open(filename, 'r')
tmp = 0
count = 0
no_lg = 0
legw = []
alarm_pod=""
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl get pods -n ', 0, 1000)
        if x1 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        x1 = q.find('No resources ', 0, 100)
        if x1 != -1:
            break
        else:
            count = 1
    else:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x1 = q.find('legacygw', 0, 1000)
            alarm=q.find('alarmhandler',0,1000)
            if x1 != -1:
                x2 = []
                x2 = q.split()
                legw.append(x2[0])
            if alarm!=-1:
                x2 = []
                x2 = q.split()
                alarm_pod=x2[0]
        else:
            break
tmp = 0
count = 0
dd = 0
helmget=''
f = open(filename, 'r')
for line in f:
    if tmp == 0 and count == 0:
        x1 = line.find('helm list -n', 0, 1000)
        if x1 != -1:
            tmp = 1
            g = ''
            g += line[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 4
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if line.isspace()==False and line.find("NAME",0,100)!=-1:
            count = 1
    elif tmp == 1 and count == 1:
        x1 = line.find(string_val, 0, 100)
        if x1 == -1:
            dd = 1
            x2 = []
            x2 = line.split()
            bvn=x2[8]
            if bvn.find('cnf',0,1000)!=-1:
                helmget+=x2[0]
                print(helmget)
                break
        else:
            break
f.close()
for j in range(len(legw)):
    var="kubectl -n " + ns + " exec -it " + legw[j] + " -c legacygw -- ip a" + "\n"
    chan.send(var)
    time.sleep(2)
    var="kubectl -n " + ns + " exec -it " + legw[j] + " -c legacygw -- ip route" + "\n"
    chan.send(var)
    time.sleep(2)
    var="kubectl -n " + ns + " exec -it " + legw[j] + " -c legacygw -- cat /proc/net/sctp/assocs" + "\n"
    chan.send(var)
    time.sleep(2)
    var="kubectl -n " + ns + " logs " + legw[j] + " -c ipmanager" + "\n"
    chan.send(var)
    time.sleep(2)
var='kubectl get svc -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get events -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get secrets -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get certificates -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'helm list -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get deployments -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get replicasets -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get statefulset -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get cronjob -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get job -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get ingress -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl get daemonset -n ' + ns + '\n'
chan.send(var)
time.sleep(2)
var = 'kubectl exec -it ' + alarm_pod + " -n "+ ns + " -c alarmhandler -- get alarmtable" + '\n'
chan.send(var)
time.sleep(2)
resp = chan.recv(999999999)


output = resp.decode('ascii')

f = open(filename, 'a+')
f.write(output)
f.close()
print(output)

if helmget!="":
    var='helm get values ' + helmget + ' -n ' + ns + '\n'
    chan.send(var)
    time.sleep(2)
    resp1 = chan.recv(99999999)
    buff2 =""
    buff2 += resp1.decode('ascii')
    helmfile = 'Helm_Values_File' + str_current_datetime + '.log'
    f2 = open(helmfile, 'w')
    f2.write(buff2)
    f2.close()
    print(buff2)


ssh.close()
r = ''
r += \
    "\n\n------------------------KUBERNETES NODES-----------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 1
flag = 0
master = 0
worker = 0
ready = []
notReady = []
schDis=[]
unk=[]
for line in f:
    line1 = []
    line1 = line.split()
    if tmp == 1 and flag == 1:
        if line1[1] == 'Ready':
            val = ''
            val += line1[0]
            r+= val + ' is in Ready state' + '\n'
            ready.append(val)
            x = line1[2]
            if x.find('worker', 0, 100) != -1:
                worker += 1
            else:
                master += 1
        elif line1[1] == 'NotReady':
            val = ''
            val += line1[0]
            r+= val + ' is Not in Ready state' + '\n'
            notReady.append(val)
            x = line1[2]
            if x.find('worker', 0, 100) != -1:
                worker += 1
            else:
                master += 1
        elif line1[1]=="SchedulingDisabled":
            val = ''
            val += line1[0]
            r+= val + ' is in SchedulingDisabled state' + '\n'
            schDis.append(val)
            x = line1[2]
            if x.find('worker', 0, 100) != -1:
                worker += 1
            else:
                master += 1
        elif line1[1]=="Unknown":
            val = ''
            val += line1[0]
            r+= val + ' is in Unknown state' + '\n'
            unk.append(val)
            x = line1[2]
            if x.find('worker', 0, 100) != -1:
                worker += 1
            else:
                master += 1
        else:
            break
    elif tmp==0 and flag==0:
        if line.find("kubectl get nodes -o wide",0,100)!=-1:
                tmp=1
    elif tmp == 1 and flag == 0:
        if line.isspace()==False and line.find("NAME",0,1000)!=-1:
            flag=1
r +="\n\nReady Nodes: \n\n"
if len(ready) == 0:
    r +="\nNo Nodes are in Ready state\n\n"
else:
    for i in range(len(ready)):
        r += ready[i]
        r += '\n'
r +="\n\nNot Ready Nodes: \n\n"
if len(notReady) == 0:
    r +="\nNo Nodes are in Not Ready state\n\n"
else:
    for i in range(len(notReady)):
        r += notReady[i]
        r += '\n'
r +="\n\nScheduling Disabled Nodes: \n\n"
if len(schDis) == 0:
    r +="\nNo Nodes are in Scheduling Disabled state\n\n"
else:
    for i in range(len(schDis)):
        r += schDis[i]
        r += '\n'
r +="\n\nUnknown State Nodes: \n\n"
if len(unk) == 0:
    r +="\nNo Nodes are in Unknown state\n\n"
else:
    for i in range(len(unk)):
        r += unk[i]
        r += '\n'
tmp = 0
count = 0
no = 0
r +="\n\n------------------------SMSF MESH----------------------------\n\n"
f = open(filename, 'r')
for q in f:
    x1 = q.find('kubectl get SmsfMesh -n', 0, 100)
    if tmp == 0 and count==0:
        if x1 != -1:
            tmp = 1
    elif tmp == 1 and count==0:
        if q.isspace()==False:
            count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                no = 1
                break
    elif tmp==1 and count==1 and no==0:
        if q.find("mesh",0,1000)!=-1:
            x2=[]
            x2=q.split()
            r+="\nSmsfMesh is in " + x2[1] + " state\n"
            break
if no == 1:
    r +="\nSmsf Mesh is not present\n\n"
tmp = 0
count=0
no = 0
r +="\n\n-------------------------ISTIOOPERATOR--------------------\n\n"
f = open(filename, 'r')
for q in f:
    x1 = q.find('kubectl get IstioOperator -n', 0, 100)
    if tmp == 0 and count==0:
        if x1 != -1:
            tmp = 1
    elif tmp == 1 and count==0:
        if q.isspace()==False:
            count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                no = 1
                break
    elif tmp==1 and count==1 and no==0:
        if q.find("istio",0,1000)!=-1:
            x2=[]
            x2=q.split()
            r+="\nIstioOperator is in " + x2[1] + " state\n"
            break
if no == 1:
    r +="\nIstioOperator is not present\n\n"
tmp = 0
count = 0
r +="\n\n-------------------------PODS------------------------------\n\n"
f = open(filename, 'r')
po = 0
run = []
err = []
comp = []
crash = []
init=[]
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get pods ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        x4 = q.find('-o wide', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1 and x4 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 7
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo pods available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            po += 1
            x2 = []
            x2 = q.split()
            r +=(x2[0] + ' :' + '\n' + x2[1] + '\n' + 'Pod is in ' + x2[2] + 'State\n\n\n')
            mn=x2[2]
            if x2[2]=='Running':
                run.append(x2[0])
            elif x2[2]=='Error' or x2[2].find("Error",0,100)!=-1 or x2[2].find("error",0,100)!=-1:
                err.append(x2[0])
            elif x2[2]=='Completed':
                comp.append(x2[0])
            elif x2[2]=='CrashLoopBackOff':
                crash.append(x2[0])
            elif mn.find("/",0,100)!=-1:
                init.append(x2[0])
        else:
            break
r +="\n\n\nPODS IN RUNNING STATE :\n\n"
if len(run) > 0:
    for i in range(len(run)):
        r += run[i] + '\n'
else:
    r += 'No Pods in Running state\n'
r +="\n\n"
r +="\n\n\nPODS IN ERROR STATE :\n\n"
if len(err) > 0:
    for i in range(len(err)):
        r += err[i] + '\n'
else:
    r +="No Pods in Error state\n"
r +="\n\n"
r +="\n\n\nPODS IN COMPLETED STATE :\n\n"
if len(comp) > 0:
    for i in range(len(comp)):
        r += comp[i] + '\n'
else:
    r += 'No Pods in Completed state\n'
r +="\n\n"
r +="\n\n\nPODS IN INIT STATE :\n\n"
if len(init) > 0:
    for i in range(len(init)):
        r += init[i] + '\n'
else:
    r += 'No Pods in Init state\n'
r +="\n\n"
r +="\n\n\nPODS IN CRASH-LOOP-BACKOFF STATE :\n\n"
if len(crash) > 0:
    for i in range(len(crash)):
        r += crash[i] + '\n'
else:
    r += 'No Pods in Running state\n'
r +="\n\n"


tmp = 0
count = 0
r += \
    "\n\n-------------------------IP MANAGER------------------------------\n\n"
if len(legw) != 0:
    f = open(filename, 'r')
    y=-1
    b=0
    c=0
    d=0
    e=0
    leg_num=0
    for q in f:
        #print("\nq: ",q)
        x1 = q.find('kubectl -n ', 0, 1000)
        x2 = q.find('logs ', 0, 100)
        x3 = q.find('-c ipmanager', 0, 1000)
        if x1 != -1 and x2 != -1 and x3 != -1:
            b=1
            d=1
            y+=1
            print("Inside IP manager 1st Option")
            continue
        elif x1!=-1 and x2!=-1 and x3==-1:
            c=1
            b=1
            print("Inside IP manager 2nd Option")
        if c==1:
            x5=q.find('ipmanager', 0, 1000)
            if x5!=-1:
                y+=1
                d=1
                continue
        if d==1:
            if leg_num>len(legw):
                break
            if q.find('"Done."}',0,1000)!=-1:
                r+="\n" + legw[y] + " : IP Manager is OK"
                b=0
                c=0
                d=0
                e=1
            if q.find("kubectl -n ",0,1000)!=-1 or q.find("NAME",0,1000)!=-1 or q.find("No resources found in ",0,1000)!=-1:
                r+="\n" + legw[y] + " : IP Manager is Not OK"
                e=1
                b=0
                c=0
                d=0
            if e==1:
                leg_num+=1
                e=0
        if q.find("kubectl get svc -n",0,1000)!=-1:
            break
else:
    r +="\n\n\nNo Legacy Gw Available\n\n\n"
tmp = 0
count = 0
r +="\n\n-------------------------SVC--------------------------------\n\n"
f = open(filename, 'r')
ser = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get svc ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo Services available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x2 = []
            ser += 1
            x2 = q.split()
            r+="\n\nService name: " + x2[0] + "\nService type:  " + x2[1] + "\nCluster IP:  " + x2[2] + "\nExternal IP:  " + x2[3] + "\nPort(s):  " + x2[4]
        else:
            break
tmp = 0
count = 0
r +="\n\n-------------------------UNHEALTHY EVENTS--------------------------------\n\n"
f = open(filename, 'r')
no = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get events ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        count = 1
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x2 = []
            x2 = q.split()
            if x2[1] == 'Warning':
                no = 1
                r +="\n\nLast seen: " + x2[0] + '\nType: ' + x2[1] \
                + '\nReason: ' + x2[2] + '\nObject: ' + x2[3] \
                + '\nMessage: ' + x2[4]
        else:
            break
if no == 0:
    r +="\n\nNo Unhealthy Events\n\n"
r +="\n\n--------------------------SECRETS----------------------------------------\n\n"
f = open(filename, 'r')
se = 0
tmp = 0
count = 0
samp=[]
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get secrets ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo Secrets available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x2 = []
            x2 = q.split()
            se+=1
            if len(x2)<4:
                for ln in range(len(x2)):
                    samp.append(x2[ln])
                if len(samp)==4:
                    r+="\n\n\nSecret name: " + samp[0] + "\nSecret type: "+ samp[1] + '\nData:  ' + samp[2] + '\nAge:  ' + samp[3] + "\n\n"
                    samp=[]
            else:
                r+="\n\n\nSecret name: " + x2[0] + "\nSecret type: "+ x2[1] + '\nData:  ' + x2[2] + '\nAge:  ' + x2[3] + "\n\n"
        else:
            break
r +="\n\n--------------------------CERTIFICATES----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
red = []
nor = []
samp=[]
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get certificates ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo Certificates available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x2 = []
            x2 = q.split()
            if len(x2)<4:
                for ln in range(len(x2)):
                    samp.append(x2[ln])
                if len(samp)==4:
                    r+="\n\n\nCertificate name: " + samp[0] + "\nReady: "+ samp[1] + '\nSecret:  ' + samp[2] + '\nAge:  ' + samp[3] + "\n\n"
                    if samp[1] == 'True':
                        red.append(samp[0])
                    else:
                        nor.append(samp[0])
                    samp=[]
            else:
                if x2[1] == 'True':
                    red.append(x2[0])
                else:
                    nor.append(x2[0])
                r +="\n\nCertificate name: " + x2[0] + '\nReady:  ' \
                + x2[1] + '\nSecret:  ' + x2[2] + '\nAge:  ' + x2[3] \
                + "\n\n"
        else:
            break
r +="\n\n\n\nCERTIFICATES IN READY STATE\n\n"
if len(red) > 0:
    for i in range(len(red)):
        r += red[i] + '\n'
    r +="\n\n"
else:
    r +="\n\nNo Certificates in Ready state\n\n"
r +="\n\n\n\nCERTIFICATES IN NOT READY STATE\n\n"
if len(nor) > 0:
    for i in range(len(nor)):
        r += nor[i] + '\n'
    r +="\n\n"
else:
    r +="\n\nNo Certificates in Not Ready state\n\n"
r +="\n\n--------------------------HELM LIST-----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
dd = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('helm list -n', 0, 1000)
        if x1 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 4
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False and q.find("NAME",0,100)!=-1:
            count = 1
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            dd = 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nNamespace:  ' + x2[1] \
            + '\nStatus: ' + x2[7] + "\n\n"
        if x2[8].find('cnf',0,1000)!=-1:
            helmget=x2[0]
        elif dd != 1:
            r +="\n\nNo Resource available\n"
            break
        else:
            break
r +="\n\n--------------------------DEPLOYMENTS--------------------------------------\n\n"
f = open(filename, 'r')
dep = 0
tmp = 0
count = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get deployments ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo Deployments available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            dep += 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nReady:  ' + x2[1] \
            + '\nUp to Date:  ' + x2[2] + '\nAvailable:  ' + x2[3] \
            + ' \nAge: ' + x2[4] + "\n\n"
        else:
            break
r +="\n\n--------------------------REPLICA-SETS-----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
repl = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get replicasets ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                r +="\n\nNo Replica-Sets available\n"
                break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            repl += 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nDesired:  ' + x2[1] \
            + '\nCurrent:  ' + x2[2] + '\nReady:  ' + x2[3] \
            + '\nAge: ' + x2[4] + "\n\n"
        else:
            break
r +="\n\n--------------------------STATEFUL-SET-----------------------------------------\n\n"
f = open(filename, 'r')
ss = 0
tmp = 0
count = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get statefulset ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
        y = q.find('No resources found in', 0, 100)
        if y != -1:
            r +="\n\nNo Stateful-Set available\n"
            break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            ss += 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nReady:  ' + x2[1] \
            + '\nAge:  ' + x2[2] + "\n\n"
        else:
            break
r +="\n\n--------------------------CRONJOB-----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
cj = 0
count = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get cronjob ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            #count = 1
            y = q.find('No resources found in', 0, 100)
            if y != -1:
                count=1
                r +="\n\nNo CronJob available\n"
                break
            elif q.find("NAME",0,1000)!=-1:
                count=1
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            cj += 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nSchedule:  ' + x2[1] \
            + x2[2] + x2[3] + x2[4] + x2[5] + '\nSuspend: ' + x2[6] \
            + '\nActive: ' + x2[7] + '\nLast schedule: ' + x2[8] \
            + '\nAge:  ' + x2[9] + "\n\n"
        else:
            break
r +="\n\n------------------------------------JOB-----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get job ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
        y = q.find('No resources found in', 0, 100)
        if y != -1:
            r +="\n\nNo Jobs available\n"
            break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nCompletions:  ' + x2[1] \
            + '\nDuration: ' + x2[2] + '\nAge:  ' + x2[3] \
            + "\n\n"
        else:
            break
r +="\n\n------------------------------------LEGACYGW IP A-----------------------------------------\n\n"
f = open(filename, 'r')
if len(legw) > 0:
    r +="\nLegacy Gw IP :-\n"
    count = 0
    y=-1
    b=0
    c=0
    d=0
    e=0
    w=0
    if len(legw) > 0:
        for q in f:
            #print("\nq: ",q)
            x1 = q.find('kubectl -n', 0, 1000)
            x2 = q.find('exec -it', 0, 1000)
            x3 = q.find('-- ip a', 0, 1000)
            if x1 != -1 and x2 != -1 and x3 != -1:
                b=1
                d=1
                #print("\nb: ",b)
                #print("\nd: ",d)
                y+=1
                w+=1
            elif x1!=-1 and x2!=-1 and x3==-1:
                c=1
                b=1
                #print("\nc: ",c)
                #print("\nb: ",b)
            if c==1:
                #print("\nInside c\n")
                x5=q.find('-- ip a', 0, 100)
                if x5!=-1:
                    y+=1
                    d=1
                    w+=1
            if b==1 and e==0:
                g=""
                g += q[::-1]
                q1 = []
                q1 = g.split()
                q3=[]
                q3=q.split()
                ik=0
                bg=""
                while(q3[ik]!="kubectl" and ik<len(q3)):
                    bg+=q3[ik] + " "
                    ik+=1
                string_val=bg
                e=1
                continue
            else:
                if count == 0 and d==1:
                    x1 = q.find('net', 0, 1000)
                    x2 = q.find('BROADCAST', 0, 1000)
                    if x1 != -1 and x2 != -1:
                        count += 1
                elif count>0:
                    count+=1
                    if count == 3:
                        x2 = []
                        x2 = q.split()
                        r += '\n' + legw[y] + " (Sigtran " + str(w) + " )" +  " : " + x2[1] + '\n'
                        count = 0
                        w+=1
            if b==1 and q.find(string_val,0,1000)!=-1:
                b=0
                c=0
                d=0
                e=0
                w=0
            if q.find("kubectl get svc -n",0,1000)!=-1:
                break
else:
    r +="\n\n\nNo Legacy Gw Pod Available\n\n\n"
r +="\n\n------------------------------------LEGACYGW IP ASSOCIATIONS-----------------------------------------\n\n"
f = open(filename, 'r')
flag = 0
if len(legw) > 0:
    flag = 0
    y=-1
    b=0
    c=0
    d=0
    e=0
    tmp=0
    bo=0
    for q in f:
        x1 = q.find('kubectl -n', 0, 1000)
        x2 = q.find('exec -it', 0, 1000)
        x3 = q.find('-- cat /proc/net/sctp/assocs', 0, 1000)
        if x1 != -1 and x2 != -1 and x3 != -1:
            b=1
            d=1
            y+=1
        elif x1!=-1 and x2!=-1 and x3==-1:
            c=1
            b=1
        if c==1:
            x5=q.find('-- cat /proc/net/sctp/assocs', 0, 100)
            if x5!=-1:
                y+=1
                d=1
        if b==1 and e==0:
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            q3=[]
            q3=q.split()
            ik=0
            bg=""
            while(q3[ik]!="kubectl" and ik<len(q3)):
                bg+=q3[ik] + " "
                ik+=1
            string_val=bg
            print("\nSTRING VAL: " + string_val + "\n")
            e=1
            continue
        else:
            if d==1 and flag==0 and q.isspace()==False:
                flag=1
                continue
            elif flag==1 and tmp==0:
                x=("\n" + legw[y] + " : " + q)
                r+=("\n" + legw[y] + " : \n" + q)
                tmp=1
                continue
            elif tmp==1 and flag==1:
                if bo==0 and q.find(string_val,0,1000)!=-1:
                    r+=("\nNo associations\n")
                    #x="\n" + legw[y] + " : " + "No associations\n"
                    b=0
                    c=0
                    d=0
                    e=0
                    flag=0
                    tmp=0
                    bo=0
                else:
                    bo=1
                    if q.find(string_val,0,1000)!=-1:
                        b=0
                        c=0
                        d=0
                        e=0
                        flag=0
                        tmp=0
                        bo=0
                    else:
                        r+=("\n" + q)
                        x="\n" + q
                        bo=1
        if q.find("kubectl get svc -n",0,1000)!=-1:
            break
else:
    r+="\n\n\nNo Legacy Gw Pod Available\n\n\n"
r +="\n\n\n------------------------------------INGRESS-----------------------------------------\n\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
ing = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get ingress ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
        y = q.find('No resources found in', 0, 100)
        if y != -1:
            r +="\n\nNo Ingress available\n"
            break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            ing += 1
            x2 = []
            x2 = q.split()
            r +="\n\nNamespace: " + x2[0] + '\nName:  ' + x2[1] \
                + '\nClass: ' + x2[2] + "\n\n"
        else:
            break
r +="\n\n------------------------------------DAEMONSET-----------------------------------------\n\n"
f = open(filename, 'r')
tmp = 0
count = 0
dae = 0
for q in f:
    if tmp == 0 and count == 0:
        x1 = q.find('kubectl ', 0, 100)
        x2 = q.find('get daemonset ', 0, 100)
        x3 = q.find('-n ', 0, 100)
        if x1 != -1 and x2 != -1 and x3 != -1:
            tmp = 1
            g = ''
            g += q[::-1]
            q1 = []
            q1 = g.split()
            w = 0
            res = []
            index = 5
            for k in range(index, len(q1)):
                dum = ''
                dum += q1[k]
                res.append(dum[::-1])
            res.reverse()
            string_val = ' '.join(map(str, res))
    elif tmp == 1 and count == 0:
        if q.isspace()==False:
            if q.find("NAME",0,100)!=-1:
                count = 1
        y = q.find('No resources found in', 0, 100)
        if y != -1:
            r += "\n\nNo Daemonset available\n"
            break
    elif tmp == 1 and count == 1:
        x1 = q.find(string_val, 0, 100)
        if x1 == -1:
            dae += 1
            x2 = []
            x2 = q.split()
            r +="\n\nName: " + x2[0] + '\nDesired: ' + x2[1] \
                + '\nCurrent: ' + x2[2] + '\nReady: ' + x2[3] \
                + '\nUp to Date: ' + x2[4] + '\nAvailable: ' + x2[5] \
                + '\nNode Selector: ' + x2[6] + '\nAge: ' + x2[7] \
                + "\n\n"
        else:
            break
r +="\n\n--------------------------------------------------------------------------------\n\n"
r +="\nCLUSTER RESOURCES:\n\nMaster Nodes                 :"+ str(master) + '\nWorker Nodes                 :' + str(worker) + '\nDeployments                  :' + str(dep) \
    + '\nServices                     :' + str(ser) \
    + '\nIngresses                    :' + str(ing) \
    + '\nStatefulSets                :' + str(ss) \
    + '\nPods                         :' + str(po) \
    + '\nDaemonSets                   :' + str(dae) \
    + '\nReplicaSets                  :' + str(repl) \
    + '\nCronJobs                     :' + str(cj) + '\n' \
    + 'Secrets                      :' + str(se) + '\n'
bv = 'report_' + str_current_datetime + '.log'
newFile = open(bv, 'w')
newFile.write(r)
newFile.close()
f.close()
