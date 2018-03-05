from ctypes import c_int32 
import urllib.request
import urllib.parse
import re
import json
import webbrowser


def rshift(val, n): 
    return val >> n if val >= 0 else (val+0x100000000) >> n


class google_handler():
    def __init__(self, wd):
        self.wd = wd
        self.TKK = self.get_TKK()
        self.tk = self.vq()

    def get_TKK(self):
        url = 'https://translate.google.cn/#auto/zh-CN/' + self.wd
        header = {'user-agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        req = urllib.request.Request(url, headers=header)
        rsp = urllib.request.urlopen(req).read().decode()
        reg = re.compile(r"TKK=eval\('\(\(function\(\)\{(.*?)\}")
        res = re.findall(reg, rsp)
        if len(res) == 1:
            res = res[0]
            reg = re.compile(r'var a\\x3d(\d+);var b\\x3d([-]{0,1}\d+);return (\d+)[+]\\x27[.]\\x27')
            res = re.findall(reg, res)
            if len(res) == 1:
                a, b, c = res[0]
                tk = '.'.join([c, str(int(a) + int(b))])
                return tk
        return 

    def tq(self, a, b):
        c = 0
        while c < (len(b) - 2):
            d = b[c+2]
            d = (ord(d[0])-87) if 'a' <= d else int(d)
            d = c_int32(rshift(a, d)).value if "+" == b[c+1] else c_int32(a << d).value
            a = a + c_int32(d & 4294967295).value if '+' == b[c] else c_int32(a ^ d).value
            c += 3
        return a

    def vq(self):
        b = self.TKK
        d = b.split('.')
        b = int(d[0]) | 0
        a = self.wd
        f = 0
        e = []
        g = 0
        c = '&tk='
        while g < len(a):
            l = ord(a[g])
            if 128 > l:
                e.append(l)
                f += 1
            else:
                if 2048 > l:
                    e[f] = c_int32(l >> 6).value | 192
                    f += 1
                else:
                    if (55296 == c_int32(l & 64512).value and 
                        g + 1 < a.length and 56320 == c_int32(ord(a[g + 1]) & 64512).value):
                        g += 1
                        l = 65536 + c_int32((l & 1023) <<
                                            10).value + (ord(a[g]) & 1023)
                        e[f] = c_int32(l >> 18).value | 240
                        f += 1
                        e[f] = c_int32(l >> 12).value & 63 | 128
                        f += 1
                    else:
                        e[f] = c_int32(l >> 12).value | 224
                        f += 1
                        e[f] = c_int32(l >> 6).value & 63 | 128
                        f += 1

                    e[f] = c_int32(l >> 6).value & 63 | 128
                    f += 1
            g += 1
        a = b
        f = 0
        while f < len(e):
            a += e[f]
            a = self.tq(a, "+-a^+6")
            f += 1
        a = self.tq(a, "+-3^+b+-f")
        a  = c_int32(a ^ int(d[1])).value
        #0 > a & (a = (a & 2147483647) + 2147483648)
        if a < 0:
            a = c_int32(a & 2147483647).value + 2147483648
        a = int( a % 1E6)
        return c + (str(a) + "." + str(a ^ b))

    def translate(self):
        res = self.trans_full()
        res_jsn = json.loads(res)[0]
        res = ''.join(i[0] for i in res_jsn if i[0])
        return res

    def trans_full(self):
        url = ('https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=en&dt=at&'
        'dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk={}&q={}')
        url = url.format(self.tk, urllib.parse.quote(self.wd, safe=''))
        #print(url)
        header = {'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        req = urllib.request.Request(url, headers=header)
        rsp = urllib.request.urlopen(req).read().decode()
        return rsp

    def gtranslate(self):
        url = 'https://translate.google.cn/#auto/zh-CN/{}'
        url = url.format(urllib.parse.quote(self.wd, safe=''))
        webbrowser.open_new(url)


if __name__ == '__mail__':
    text = '''I was wondering if after all these years you'd like to meet
    They say that time's supposed to heal ya, but I ain't done much healing'''
    G = google_trans(text)
    print(G.translate())
