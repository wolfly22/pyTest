import win32gui
import win32con
from win32gui import *
import win32clipboard 
import chardet

titles = set()
def foo(hwndd,sdd):
    #去掉下面这句就所有都输出了，但是我不需要那么多
    # if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
    str = GetWindowText(hwndd)
    st = win32gui.GetClassName(hwndd)
    print( "窗口句柄:%s----窗口标题:%s------%s"  %(hwndd,str,st))
    titles.add( str )

def test():
    EnumWindows(foo,0)
    lt = [t for t in titles if t]
    # lt.sort()
    for t in lt:
        print( t )


def dumpWindow():
    win = win32gui.FindWindow('Notepad','aa.txt - 记事本')
    tid = win32gui.FindWindowEx( win,None,'Edit',None )
    print( 'win:%d   tid:%d' %(win,tid) )
    win32gui.SendMessage(tid,win32con.WM_SETTEXT,None,'AAAAAAAA')
    win32gui.PostMessage(tid,win32con.WM_KEYDOWN,win32con.VK_RETURN,0) 

#读取剪切板
def clipboard():
    win32clipboard.OpenClipboard()
    b = win32clipboard.GetClipboardDataHandle(win32clipboard.CF_TEXT)
    

if __name__ == "__main__":
    # dumpWindow()
    # test()
    clipboard()