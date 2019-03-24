# VLSM Calculator made by Noé Camacho Lizárraga in Python 3.6

import os
from netaddr import *
from prettytable import PrettyTable
from colorama import init, Fore, Style, Back
import pprint

#class IPNetwork(BaseIP, IPListMixin):

def clearTerminal():
    if os.name == 'nt':
        os.system('cls')
        pass
    else:
        os.system('clear')
        pass
    pass

# 'nt' for Windows, posix' for linux

def validateIP(ip):
    return ip.valid_ipv4(ip)

def printHeader():
    print('\n\n')
    print(Style.BRIGHT,Fore.WHITE,Back.BLUE)
    print("                                                ")
    print("         | | | |  CALCULADORA VLSM | | | |      ")
    print("             by Noé Camacho Lizárraga           ")
    print("                                               ", Style.RESET_ALL, '\n\n')

def test(ip):
        print("ITER HOSTS:", ip.iter_hosts)
        print("IP LAST:",ip.last)
        print("IP NEXT:",ip.next(1))
        # print(ip.netmask.bits())
        print("BITS USADOS RED",ip.netmask.bits())
        print("BROADCAST", ip.broadcast.bits())
        print("BITS DE RED", ip.prefixlen/8)
        print("IP_ADD:",ip.__iadd__(1))
        network = ip.netmask.bits()
        print("SUPERNET:",ip.subnet(ip.prefixlen))
        

        stringtemp = ip.__str__()
        word = []
        word.append(stringtemp.split('.'))
        print("STRING;",word)
        
        
        pass

def printTable(table, majorNet, neededHosts, allocatedHosts):
    clearTerminal()
    ipTemp = IPNetwork(majorNet)
    print('\n\n')
    print(Style.BRIGHT,Fore.WHITE,Back.GREEN)
    print("                                                ")
    print("         | | | |  SUBNETEO EXITOSO | | | |      ")
    print("                                               ", Style.RESET_ALL, '\n\n')
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,Style.NORMAL,' RED PRINCIPAL:', Fore.WHITE, Back.GREEN, Style.BRIGHT,'{}'.format(ipTemp),Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,' Redes Disponibles en RED PRINCIPAL:',Fore.WHITE,Back.GREEN,Style.BRIGHT,'{}'.format(ipTemp.size - 2),Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,' Numero de direcciones IP necesarias:',Fore.WHITE, Back.GREEN,Style.BRIGHT,'{}'.format(neededHosts),Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,' Direcciones IP almacenadas en las subredes:',Fore.WHITE,Back.GREEN,Style.BRIGHT,'{}'.format(allocatedHosts),Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,' Cerca del',Fore.WHITE,Back.GREEN,Style.BRIGHT,'{}%'.format(int((allocatedHosts*100)/ipTemp.size-2)),Back.WHITE,Fore.BLACK,Style.NORMAL,'de espacio de la RED PRINCIPAL es usado',Style.RESET_ALL)    
    print(Back.WHITE, Fore.BLACK,Style.NORMAL,' Cerca del',Fore.WHITE, Back.GREEN,Style.BRIGHT,'{}%'.format(int((neededHosts*100)/allocatedHosts)),Back.WHITE,Fore.BLACK,Style.NORMAL,'de espacio de la RED SUBNETEADA es usado',Style.RESET_ALL)    
    print("\n\n")
    print(table)


def requestNets(netSize):
    hostSize = {}
    print('\n\n|  RED  | No. Hosts |')
    for hosts in range(0, netSize):
        hostSize[hosts+1] = (int(input('>   {}        '.format(hosts+1))) + 2)
    # for k, v in hostSize.items():
    #     print(k, v)
    return hostSize

def calculateNetwork(ip, hostSize, pos):
    cidr = calculateCidr(hostSize, pos)
    temp = ip
    temp2 = temp.__str__()
    temp3 = temp2.split('/')
    del(temp3[1]) 
    temp3.append(str(cidr))
    chara= '/'
    # print('TEMP3',temp3)
    # print(len(temp3))
    ip = IPNetwork(chara.join(temp3))
    # print("ip: ",ip)
    return ip 

def calculateCidr(hostSize, pos):
    for num in range(0,100):
        # print(num, 2**num)
        if (hostSize[pos] <= 2**num):
            # print("===========>",num, 2**num)
            # print('CIDR:', 32-num)
            # print('Mask:', num/8)
            # print("Host:", 32-num/8)
            return 32-num
        else:
            pass
def main():
    init()
    clearTerminal()
    printHeader()
    table = PrettyTable()
    table.field_names = ['Subred','Hosts Necesarios','Hosts Almacenados','Dirección de red', 'Rango de IP', 'Broadcast', 'CIDR', 'Máscara']
    neededHosts = 0
    allocatedHosts = 0
    try:
        majorNet = input('--> Ingresa la RED PRINCIPAL: ')
        ip = IPNetwork(majorNet)
        netSize = int(input('--> Cantidad Subredes: '))
        netDict= requestNets(netSize)
        for pos in range(0, netSize):
            ip = calculateNetwork(ip, netDict, pos+1)
            ip_list = list(ip)
            # test(ip)
            table.add_row([pos+1, netDict[pos+1]-2, ip.size-2, ip.ip, '{} - {}'.format(ip_list[1], ip[len(ip_list)-2]), ip.broadcast, '/{}'.format(ip.prefixlen), ip.netmask])
            neededHosts = neededHosts + (netDict[pos+1]-2)
            allocatedHosts = allocatedHosts + (ip.size-2)
            ip = ip.next(1)
        printTable(table,majorNet, neededHosts, allocatedHosts)
    except:
        print('\n\n',Fore.WHITE, Back.RED)
        print("                                                ")
        print("         | | | |  SUCEDIÓ UN ERROR | | | |      ")
        print("                                               ", Style.RESET_ALL, '\n\n')
    
if __name__ == "__main__":
       main()

    # print('Dirección de red(ip):', ip.ip)
    # print('Dirección de red(network):', ip.network)
    # print('Rango de IP: {} - {}'.format(ip_list[1], ip[len(ip_list)-2]))
    # print('Broadcast:', ip.broadcast)
    # print('CIDR: /',ip.prefixlen)
    # print('CIDR2:', ip.cidr)
    # print('Tamaño:', ip.size)
    # print('Máscara de red:', ip.netmask)
    # print('Máscara de host:', ip.hostmask)
    # print('Version:', ip.version)
    # print('Cantidad de Hosts:', len(ip_list))

    #print('version:{}'.format(ip.version()))
    # print('¿Cuántas subredes deseas crear?: ')
    #netSize = int(input('¿Cuántas subredes deseas crear?:'))
    #subNets = []
    #print('## Ingresa el número de hosts para cada red')
    #for network in range(1, netSize+1):
        # String formatting in `input statement` instead of a print
    #    temp = input('Red {}: '.format(network))
    #    subNets.append(temp)
    #print(subNets)

""""
[ X ] Request Major Network
[ ] Calculate the CIDR
[ ] Calculate the subnet Mask
[ ] Calculate the jump 
"""