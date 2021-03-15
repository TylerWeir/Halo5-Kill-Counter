# This program blinks the output light of an ESP8266 board.
import time
import network
import socket
import ssl

def toggle(p):
    p.value(not p.value())

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Weir Farm 2.4GHz', 'bigchicken')
        while not sta_if.isconnected():
            pass 
    print('connected to network')
    print('network config:', sta_if.ifconfig())

def halo():
    # Connect to the host. 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.getaddrinfo('www.haloapi.com', 80)[0][-1]
    client.connect(addr)

    # Request data from the host.
    path = '/stats/h5/players/EnduroCat14/matches?'
    host = 'www.haloapi.com'
    key = 'f83454ddd4fb4e4da43f9752693bf8e2'
    client.send(bytes('GET %s\r\nHost: %s\r\nOcp-Apim-Subscription-Key: %s\r\n\r\n' % (path, host, key), 'utf8'))
    
    while True:
        data = client.recv(4096)
        if data:
            print(str(data, 'utf8'))
        else:
            break
    s.close()

def run():
    do_connect()
    halo()

if __name__ == "__main__":
    run()
