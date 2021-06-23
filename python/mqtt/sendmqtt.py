import socket
import struct
import sys

def do_connect(client_id, server, port=0, topic="", message="", qos=0, user=None, password=None, ssl=False,clean_session=True):
    try:
        status=False
    
        sock = socket.socket()
        
        addr = socket.getaddrinfo(server, port)[0][-1]
        sock.connect(addr)
       
        if ssl:
            import ssl
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.verify_mode=ssl.CERT_NONE
            context.check_hostname = False
            sock = context.wrap_socket(sock,do_handshake_on_connect=False)
            
        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")
    
        sz = 10 + 2 + len(client_id)
        msg[6] = clean_session << 1
        if user is not None:
            sz += 2 + len(user) + 2 + len(password)
            msg[6] |= 0xC0
    
        i = 1
        while sz > 0x7f:
            premsg[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        premsg[i] = sz
        
        sock.send(premsg[0:i + 2])
        sock.send(msg)
    
        sock.send(struct.pack("!H", len(client_id.encode())))
        sock.send(client_id.encode())        
        
        if user is not None:
            sock.send(struct.pack("!H", len(user.encode())))
            sock.send(user.encode())
            sock.send(struct.pack("!H", len(password.encode())))
            sock.send(password.encode())               
        
        resp = sock.recv(4)
        
        if (resp[3] != 0 or resp[0] != 0x20 or resp[1] != 0x02):
            sys.stderr.write("MTQQ: Error Response %x,%x,%x,%x\n" % (resp[0],resp[1],resp[2],resp[3]))
            return(status)
        
        retain=False
        
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(message)
        if qos > 0:
            sz += 2
        #assert sz < 2097152
        if (sz < 2097152):
            i = 1
            while sz > 0x7f:
                pkt[i] = (sz & 0x7f) | 0x80
                sz >>= 7
                i += 1
            pkt[i] = sz
        
            sock.send(pkt[0:i + 1])
        
            sock.send(struct.pack("!H", len(topic.encode())))
            sock.send(topic.encode())        
        
            sock.send(message.encode())
            
            status=True
        else:
            sys.stderr.write("MQTT MSG to Large - ABORT\n")
            status=False
            
        sock.send(b"\xe0\0")
        sock.close()
            
            
    except OSError:
        # LIKELY NETWORK ERROR
        sys.stderr.write("MQTT Network issue - ABORT\n")
        status=False        
    except:
        # SOMETHING ELSE HAPPENED
        import traceback
        traceback.print_exc(file=sys.stderr)
        status=False
    
    return(status)


do_connect(client_id="TestMTQQ",server="127.0.0.1", port=1883,topic="Topic1",message='XX'.zfill(2097000))
