from urllib import request,parse
import re
from http import cookiejar
"""
账号密码需填写   自动验证码识别登陆 需要使用其他扩展包 再加处理
"""

cookie = cookiejar.CookieJar()
cookie_handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(cookie_handler)
# 替换request 默认opener
request.install_opener(opener)

login_url = 'https://accounts.douban.com/login'

def getLoginPage():
    response = request.urlopen(login_url)
    html = response.read().decode('utf-8')
    if '验证码' in html:
        dologin(html)
    else:
        login(html)

    return html

def dologin(html):
    code_pat = re.compile(r'captcha_image" src="(.*?)"')
    code_res = code_pat.search(html)
    if code_res is not None:
        code_url = code_res.group(1)
    else:
        code_url = None

    token_pat = re.compile(r'captcha-id" value="(.*?)"')
    token_res = token_pat.search(html)
    if token_res is not None:
        token = token_res.group(1)
    else:
        token = None

    if token and code_url:
        # 下载验证码图片并输入
        print(code_url)
        request.urlretrieve(code_url, 'code.png')
        code = input('请输入验证码：')

        data = {
            'form_email': '账号',
            'form_password': '密码',
            'redir': 'https://www.douban.com/',
            'captcha-solution' : code,
            'captcha-id' : token
        }

        data = parse.urlencode(data)

        headers = {
            'Content-Length': len(data)
        }

        # 发起登陆请求
        req = request.Request(url=login_url,data=bytes(data,encoding='utf-8'),headers=headers)
        response = request.urlopen(req)

        html = response.read().decode('utf-8')
        check_login(html)
    else:
        print('获取登录信息失败')

def login(html):
    data = {
        'form_email' : '1752570559@qq.com',
        'form_password' : '1234qwer',
        'redir' : 'https://www.douban.com/'
    }

    data = parse.urlencode(data)

    headers = {
        'Content-Length' : len(data)
    }

    req = request.Request(url=login_url,data=bytes(data,encoding='utf-8'),headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    check_login(html)


def check_login(html):
    if '个人主页' in html:
        print('登陆成功，继续操作')
        con = '''
            1.修改签名
            2.其它
        '''
        sign = input('输出新的签名')
        update_sign(sign)


    else:
        print('登陆失败')


# 修改签名
def update_sign(sign):
    # 发起个人首页请求
    home_url = 'https://www.douban.com/people/96640796/'
    response = request.urlopen(home_url)
    html = response.read().decode('utf-8')
    ck_pat = re.compile(r'name="ck" value="(.*?)"')
    ck_res = ck_pat.search(html)
    if ck_res is not None:
        ck = ck_res.group(1)
    else:
        print('获取ck失败')
        exit()

    data = {
        'ck' : ck,
        'signature' : sign
    }
    data = parse.urlencode(data)

    headers = {
        'Content-Length' : len(data)
    }

    sign_url = 'https://www.douban.com/j/people/96640796/edit_signature'

    req = request.Request(url=sign_url,data=bytes(data,encoding='utf-8'),headers=headers)

    response = request.urlopen(req)

    print(response.read().decode('utf-8'))

if __name__ == '__main__':
    html = getLoginPage()


