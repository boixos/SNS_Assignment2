from package import *

buffer = 8192
sync = 'ok'.encode('utf-8')

def verify(crc,recv_crc,recv_string):
    print('String Received',recv_string)
    if crc == recv_crc:
        print('CRC verified, Correct String is Recevied')
    else:
        print('CRC verification Failed, ERROR in recevied String')    


def decode_data(cipher):
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


def main():
    serv = socket.socket()
    serv.bind(('',port))
    serv.listen(5)
    while 1:
        cli,addr = serv.accept()

        cipher = cli.recv(buffer)
        cli.send(sync)
        crc = cli.recv(buffer)
        cli.send(sync)
        cipher += b'.'

        cipher, recv_crc = pickle.loads(cipher),pickle.loads(crc)

        crc,recv_string = decode_data(cipher)
        print(crc,recv_string)
        verify(crc,recv_crc,recv_string)



if __name__ == '__main__':
    main()