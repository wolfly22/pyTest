import requests
from lxml import etree
import os 
import xlwings as xw
from datetime import date,datetime,timedelta



#获取网站数据
def get_html_data( url ):
    code = requests.get( url )
    if code.status_code ==200:
        html_str = code.content.decode('gbk')
        html = etree.HTML(html_str)
        return html
    else:
        print("未响应！请确认网络连接正常or网站正常!")
        return None



#获取页面data
def read_data( url ):
    data_list = []
    html = get_html_data( url )
    if html!=None:
        tbody = html.xpath('//*[@id="ct"]/div/div[4]/table/tbody')
        trs = tbody[0].findall('tr')
        for tr in trs:
            tds = tr.itertext()
            td_list = []
            for text in tds:
                if (text!='\r\n') and (not text.startswith('\r\n')):
                    td_list.append( text )
            data_list.append( td_list )
    else:
        print("未响应！请确认网络连接正常or网站正常!")
    return data_list

#获取页面时间
def get_date( url ):
    # print("%43%" ,url )
    html = get_html_data(url)
    if html!=None:
        top_date_text = html.xpath('//*[@id="ct"]/div/div[4]/table/tbody/tr[1]/td[6]')[0].text
        top_date_text = datetime.strptime( str(top_date_text),'%Y-%m-%d %H:%M').date()
        down_date_text = html.xpath('//*[@id="ct"]/div/div[4]/table/tbody/tr[20]/td[6]')[0].text
        down_date_text = datetime.strptime( str(down_date_text),'%Y-%m-%d %H:%M').date()
        print( top_date_text,'--------',down_date_text )
        return top_date_text,down_date_text
    else:
        print("未响应！请确认网络连接正常or网站正常!")
        return None

#drop
def get_top_pages(page):
    page_list = []
    url = 'https://www.178448.com/fjzt-1.html?page='
    page_temp = 0
    #初次获取时间
    if(page_temp==0):
        page_temp = 30
        (top_date,down_date) = get_date( url+str(page_temp) )
        res = compare_date( top_date )
        #top昨日
        if( res ):
            while(res):
                page_temp -= 1
                (top_date,down_date) = get_date( url+str(page_temp))
                print("向前翻一页查找")
                #top昨日
                if(compare_date(top_date) ):
                    continue
                #top今日
                else:
                    #down昨日
                    if( compare_date(down_date) ):
                        page_list.append( page_temp )
                        break
                    #down今日
                    else:
                        continue
        #top今日
        else:
            #向后翻页
            print("向后翻页查找!")
            res = True
            while( res):
                (top_date,down_date) = get_date( url+str(page_temp+1))
                print("向后翻一页查找!")
                #top昨日
                if(compare_date( top_date )):
                    print('顶部昨日')
                    page_temp += 1
                    page_list.append( page_temp )
                    break
                #top今日
                else:
                    #down是否昨日
                    if(compare_date(down_date) ):
                        page_list.append(page_temp+1)
                        break
                    else:
                        page_temp += 1
    return page_list[0]


def get_down_page():
    down_page = 70
    bol = True
    stop_date = date.today()+timedelta(days=-3)
    print( stop_date )
    while(bol):
        url = 'https://www.178448.com/fjzt-1.html?page='
        (top_date,down_date) = get_date( url+str(down_page) )
        if( top_date > stop_date):
            print('Go >>>>>>!')
            # down_page += 1
            # (top_date,down_date) = get_date( url+str(down_page) )
            # print("#120#  向后翻一页查看")
            if(top_date>stop_date):
                if( down_date>stop_date):
                    down_page += 1
                    # continue
                elif (down_date == stop_date):
                    break
            elif(top_date==stop_date):
                break
        elif( top_date<stop_date):
            print('Go <<<<<<<!')
            down_page -= 1
            (top_date,down_date) = get_date( url+str(down_page) )
            if(top_date<stop_date):
                down_page -= 1
                # continue
            elif (top_date==stop_date):
                if( down_date==stop_date):
                    break
                elif( down_date<stop_date):
                    break
        #top_date == stop_date
        else:
            down_page -= 1
            (top_date,down_date) = get_date( url+str(down_page) )
            if(top_date==stop_date):
                down_page -= 1
            elif (top_date>stop_date):
                if( down_date==stop_date):
                    break
                elif (down_date>stop_date):
                    break
    print( down_page )
    return down_page
    

#获取数据
def  total_datas():
    page_date_list = []
    # start_page  = get_top_pages(0)
    end_page = get_down_page()
    print('------',end_page )
    url = 'https://www.178448.com/fjzt-1.html?page='
    for i in range(1,(end_page+1)):
        print( url+str(i) )
        page_date = read_data( url+str(i))
        print('正在爬取第%d页' %(i) )
        for ii in page_date:
            con_date = date.today() + timedelta(days=-3)
            # print(con_date)
            data_date = datetime.strptime(ii[5],'%Y-%m-%d %H:%M').date()
            if( data_date > con_date ):
               page_date_list.append( ii )
        print('爬取完%d页的数据' %(i) )
    print( len(page_date_list) )
    return page_date_list

    

def compare_date( datee ):
    if date!= None:
        today = date.today()
        # today += timedelta(days=-1)
        if (datee<today):
            #昨日
            return True
        else:
            #今日
            return False



def write_excle( ):
    data_list = total_datas()
    # a = datetime.today()
    # pix = str(a.year)+str(a.month)+str(a.day)+str(a.hour)+str(a.minute)
    # file_path = r'C:\ForRich' + pix + '.xlsx'
    wb = None
    sht = None
    if not os.path.exists(r'D:\ForRich.xlsx'):
        # print('初始化，创建Excle文件!')
        # excelFile = open(r'D:\ForRich.xlsx',mode='w')
        # excelFile.close()
        app = xw.App(visible=True,add_book=False )
        ex = app.books.add()
        ex.save(r'D:\ForRich.xlsx')
        ex.close()
    else:
        app = xw.App(visible=True,add_book=False )
        wb = app.books.open(r'D:\ForRich.xlsx')
        sht = wb.sheets[0]
        sht.clear()
    if data_list:
        for i in range(len(data_list)):
            strr = 'A'+ str( i+1 )
            # print( strr,'------------',data_list[i] )
            # sht.range(strr).api.Font.Name = '微软雅黑'
            # sht.range(strr).api.Font.Size = 12
            sht.range(strr).value = data_list[i]
            sht['A1:J'+str(len(data_list))].api.Font.Name = '微软雅黑'
            print('正在写入第%d行' %(i))
    wb.save()
    wb.close()
    app.quit()



if __name__ == "__main__":
    write_excle()
    # get_down_page()
    # total_datas()