


#汉字转为quoted-printed
def  str_quoted(name):
    byte_str = bytes(name.encode('utf-8'))
    list_temp = []
    hex_str = ''
    print( type(byte_str) )
    for i in byte_str:
        list_temp.append((bin(i)+'')[2:])
    print( list_temp )
    for ii in list_temp:
        if(len(ii)==8):
            hex_str += '='
            hex_str += (str(hex(int(ii[0:4],2)))[2:].upper())
            hex_str += (str(hex(int(ii[4:8],2)))[2:].upper())
        else:
            print("位数不足！")
    print( hex_str )
        
#quoted-printed转为汉字
def quoted_str(queoted_str):



if __name__ == "__main__":
    str_quoted('曹祎')