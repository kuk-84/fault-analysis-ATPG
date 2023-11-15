import copy
f=open("C:/Users/sakshi/OneDrive/Desktop/fault-analysis-ATPG/netlist.txt","r")
l=f.readlines()

def read_netlist():
    device_id=0
    for i in range (0, len(l)):
        temp=l[i]
        temp_str=''
        device=[]
        if(temp=='\n'):
            continue
        else:
            device.append(device_id) #id
            device_id=device_id+1
            
        flag=0
        z=len(temp)
        w=temp[len(temp)-1]
        for j in range (0, len(temp)):
            ewc=temp[j]
            if (j==len(temp)-1):
                if (temp[j] != ' ' or temp[j] == '\n'):
                    if(temp_str):
                        device.append(temp_str)
                        temp_str=''
                else:
                    if(temp_str):
                        device.append(temp_str)
                        temp_str=''
            elif (temp[j] !=' '):
                temp_str = temp_str + temp[j]
                
            else:
                if(temp_str):
                    device.append(temp_str)
                temp_str=''
        netlist.append(device)   
    
def convert_netlist():
    
    temp=1
    
    node_old =[]
    node_new =[]
    for i in range (0, len(netlist)):
        if (netlist[i][1][:5] == 'and2_'):
            netlist[i][1] = 3;
        elif (netlist[i][1][:3] == 'not'):
            netlist[i][1] = 1;
        elif (netlist[i][1][:6] == 'nand4_'):
            netlist[i][1] = 8;
        elif (netlist[i][1][:6] == 'nand2_'):
            netlist[i][1] = 5;
            
        for j in range (2,len(netlist[i])):
            if (netlist[i][j][:2] == 'in'):
                match=0
                for k in range (0, len(node_old)):
                    if (netlist[i][j] == node_old[k]):
                        match=1
                        break
                        
                if (match):        
                    netlist[i][j]=node_new[k]
                else:                    
                    ins.append(temp)
                    node_old.append(netlist[i][j])
                    node_new.append(temp)
                    netlist[i][j]=temp
                    temp=temp+1
                    
            elif (netlist[i][j][:3] == 'out'):
                match=0
                for k in range (0, len(node_old)):
                    if (netlist[i][j] == node_old[k]):
                        match=1
                        break
                        
                if (match):        
                    netlist[i][j]=node_new[k]
                else:                    
                    outs.append(temp)
                    node_old.append(netlist[i][j])
                    node_new.append(temp)
                    netlist[i][j]=temp
                    temp=temp+1
            else:
                match=0
                for k in range (0, len(node_old)):
                    if (netlist[i][j] == node_old[k]):
                        match=1
                        break
                        
                if (match):        
                    netlist[i][j]=node_new[k]
                else:
                    node_old.append(netlist[i][j])
                    node_new.append(temp)
                    netlist[i][j]=temp
                    temp=temp+1
    for i in range(0, len(node_old)):
        temp2 = []
        temp2.append(node_old[i])
        temp2.append(node_new[i])
        node_map.append(temp2)
    return (temp -1)


def values_initial (no_nodes):
 
    for i in range (0, no_nodes+1):
        node_values.append(-5) 

def nand_out(o,i1,i2,g):

    if (g==0):          
        if(o == -5):
            i1= i1 ; 
            i2= i2;
            o=o;      
        elif(o == 0):
            i1 = 1; i2 = 1;
        elif(o == 1):
            if (i1 == 1):  
                i2= 0;
            elif(i2 == 1): 
                    i1= 0;
            elif (i1== 0):
                i2= i2;
            elif (i2== 0):
                i1= i1;
            else:
                i1=0;
                i2=0;


    else:
        if(i1 == -5 and i2 == -5):
            o =-5;
        else:
            o1 = (i1*i2) ;
            if(abs(o1)>1): 
                o = -5;
            else:
                o = int(not(o1));
    return[o,i1,i2] 

def not_out(o,i1,g):
    if(g==0):
        if(o==-5):
            i1 = -5;
        else:    
            i1 = int(not(o))
    else:
        if(i1==-5):
            o = -5;
        else:    
            o = int(not(i1));
    return[o,i1]

def and_out(o,i1,i2,g):
    if (g==0):          
        if(o == -5):
            i1= i1 ; 
            i2= i2;
            o=o;      
        elif(o == 1):
            i1 = 1; i2 = 1;
        elif(o == 0):
            if (i1 == 1):  
                i2= 0;
            elif(i2 == 1): 
                    i1= 0;
            elif(i1== 0):
                i2= i2;
            elif(i2== 0):
                i1= i1;
            else:
                i1=0;
                i2=0;
    else:
        if(i1 == -5 and i2 == -5):
            o =-5;
        else:
            o1 = (i1*i2) ;
            if(abs(o1)>1): 
                o = -5;
            else:
                o = o1;
    return[o,i1,i2] 

def nand_4input(o,i1,i2,i3,i4,g):
    if(g==0):
        if(o==-5):
            i1 = i2 = i3 = i4 = -5;
        if(o == 0):
            i1 = i2 = i3 = i4 = 1;
        elif (o==1): 
            i1 = 0;
    elif(g==1):
        o1 = (i1*i2*i3*i4) ;
        if(abs(o1)>1): 
            o = -5;
        else:
            o = int(not(o1));
    return(o,i1,i2,i3,i4);

def main_podem(nG_C, nV):
    read_netlist()
    no_nodes = convert_netlist()
    values_initial(no_nodes)

    print(not_out(1,-5,0))
    print(and_out( 1, -5,-5, 0))
    print(nand_out( 1, -5,-5, 0))
    print(nand_4input( 1, -5, -5,-5,-5,0))
    
    
    
netlist=[]
node_values = []        
ins=[]
outs=[]
device_map = []
node_map=[[]]

Fault_Location = 'n6'
Fault_Value = 1

FL = 0
FV = Fault_Value


print ('Fault Location', Fault_Location)
print ('Fault Value', FV)
print (' ')
main_podem(Fault_Location,FV)
