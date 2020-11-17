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
        print("网站未响应!")
    return data_list

#获取页面时间
def get_date( url ):
    html = get_html_data(url)
    if html!=None:
        top_date_text = html.xpath('//*[@id="ct"]/div/div[4]/table/tbody/tr[1]/td[6]')[0].text
        top_date_text = datetime.strptime( str(top_date_text),'%Y-%m-%d %H:%M').date()
        down_date_text = html.xpath('//*[@id="ct"]/div/div[4]/table/tbody/tr[20]/td[6]')[0].text
        down_date_text = datetime.strptime( str(down_date_text),'%Y-%m-%d %H:%M').date()
        # print( top_date_text,'--------',down_date_text )
        return top_date_text,down_date_text
    else:
        print("网站未响应!")
        return None



def get_down_page():
    down_page = 70
    bol = True
    stop_date = date.today()+timedelta(days=-2)
    print('准备爬取',stop_date,'之前的数据！' )
    while(bol):
        url = 'https://www.178448.com/fjzt-1.html?page='
        (top_date,down_date) = get_date( url+str(down_page) )
        if( top_date > stop_date):
            print('Go >>>>>>!')
            if(top_date>stop_date):
                if( down_date>stop_date):
                    down_page += 1
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
    print('需压爬取1-%d页的数据!' %(down_page))
    return down_page
    

#获取数据
def  total_datas():
    page_date_list = []
    end_page = get_down_page()
    url = 'https://www.178448.com/fjzt-1.html?page='
    for i in range(1,(end_page+1)):
        page_date = read_data( url+str(i))
        for ii in page_date:
            con_date = date.today() + timedelta(days=-2)
            data_date = datetime.strptime(ii[5],'%Y-%m-%d %H:%M').date()
            if( data_date > con_date ):
               page_date_list.append( ii )
        print('已经爬取完第%d页的数据     next↓' %(i) )
    return page_date_list



def write_excle( ):
    data_list = total_datas()
    wb = None
    sht = None
    if not os.path.exists(r'D:\ForRich.xlsx'):
        app = xw.App(visible=True,add_book=False )
        wb = app.books.add()
        wb.save(r'D:\ForRich.xlsx')
        sht = wb.sheets[0]
        sht.clear()
    else:
        app = xw.App(visible=True,add_book=False )
        wb = app.books.open(r'D:\ForRich.xlsx')
        sht = wb.sheets[0]
        sht.clear()
    if data_list:
        for i in range(len(data_list)):
            strr = 'A'+ str( i+1 )
            sht.range(strr).value = data_list[i]
            sht['A1:J'+str(len(data_list))].api.Font.Name = '微软雅黑'
            print('正在写入excel表中第%d行' %(i))
    wb.save()
    wb.close()
    app.quit()


if __name__ == "__main__":
    write_excle()