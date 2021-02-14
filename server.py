from package import *
from _thread import *
import threading,subprocess

buffer = 8192
sync = 'ok'.encode('utf-8')

def verify(crc,recv_crc,recv_string,cli,addr):
    print('String Received',recv_string)
    if crc == recv_crc:
        print('CRC verified, Correct String is Recevied from SENDER:',addr, '\n')
        cli.send(sync)
    else:
        print('CRC verification Failed, ERROR in recevied String')
           


def DecData(cipher):
    data = np.dot(CIPHER_MATRIX_INV, cipher)
    # print(data)
    data = np.reshape(data,(data.shape[0]*data.shape[1]),'F')
    s = ''
    # print(DECODING_RULE)
    # print(data)

    for i in range(data.shape[0]):
        s += DECODING_RULE[data[i]]
    
    crc = generate_crc(s.rstrip())
    return crc,s


def threaded(cli,addr):
    while 1:
        # cli,addr = serv.accept()
        cipher = cli.recv(buffer)
        cli.send(sync)
        crc = cli.recv(buffer)
        cli.send(sync)
        cipher += b'.'

        cipher, recv_crc = pickle.loads(cipher), pickle.loads(crc)
        # print(mod2div(recv_crc, key))
        crc, recv_string = DecData(cipher)
        # print(crc, recv_string)
        verify(crc, recv_crc, recv_string,cli,addr)

def handl(serv):
    while 1:
        cli,addr = serv.accept()
        start_new_thread(threaded,(cli,addr))

def main():
    global port
    serv = socket.socket()
    try:
        serv.bind(('',port))
    except:
        print('Binding Failed, Try d/f port')
    serv.listen(5)
    # while 1:
        # cli,addr = serv.accept()
    start_new_thread(handl, (serv,))

    print('HIT ENTER To close SERVER')    
    input()
    print('Closing SERVER...')
    serv.close()


if __name__ == '__main__':
    main()
