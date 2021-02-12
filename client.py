from package import *

def data_padding(data):
    if len(data)%3 == 0:
            1# return data
    else:    
        while len(data)%3 != 0:
            data = data + ' '
    data = np.array([ENCODING_RULE[data[i]] for i in range(len(data))])        
    data = np.reshape(data, (3, len(data)//3), 'F')
    return data

def encode_data(input_string):
    data = data_padding(input_string)
    print(data)
    cipher = np.dot(CIPHER_MATRIX,data)
    # print(cipher)
    crc = generate_crc(input_string)
    # print(crc)

    return pickle.dumps(crc), pickle.dumps(cipher)


def main():
    serv = socket.socket()
    try:
        serv.connect(("localhost",port))
    except:
        print('Server Dowm')  
        sys.exit(0)
    while 1:    
        input_string = input()
        if input_string.isupper():
            1
        else:
            print('Enter String in UPPERCASE')  
            sys.exit(0)  
        i=1
        while i:        
            crc,cipher = encode_data(input_string)   

            serv.send(cipher)
            t = serv.recv(2).decode()
            print('Cipher sent to server: ',t)

            serv.send(crc) 
            t = serv.recv(2).decode()
            print('CRC sent to server: ',t)
            t = serv.recv(2).decode()
            if t == 'ok':
                print('String sent Successfully')
                i=0
            if t == '':
                print('ERROR sending string')
                print('Want to send again? Y/N')
                q = input()
                if q == 'N':
                    i=0

        
    serv.close

if __name__ == "__main__":
    main()