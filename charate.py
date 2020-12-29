


#汉字转为quoted-printed
def str_quoted(name):
    byte_str = bytes(name.encode('utf-8'))
    list_temp = []
    hex_str = ''
    # print( type(byte_str) )
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
    bin_list = []
    print( len(queoted_str))
    while( len(queoted_str)!=0 ):
        bin_list.append(queoted_str[1:3])
        queoted_str=queoted_str[3:]
    print( bin_list )
    



if __name__ == "__main__":
    # str_quoted('曹祎')
    quoted_str('=E6=9B=B9=E7=A5=8E')