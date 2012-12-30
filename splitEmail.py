# -*- coding: utf-8 -*-
#author:         gavin
#created:        2012-11-8
#modify          2012-11-30

import re
import os
import sys
import collections
class SplitEmail:
    '''
    首先通过当前目录下的词典建立字典树
    通过正则表达式分解邮件中的英文单词和汉字
    然后逐字检测可否组成字典中存在的单词 或 词组以达到简单的分词效果
    '''
    def __init__(self):
        self.regex = re.compile(r"[\w-]+|[\x80-\xff]{3}")
        self.wordlist = {'normal': [], 'trash': []}
        self.maildic = {'normal': {}, 'trash': {}}
        self.ratio = {}
        self.normalnum = 0                                          #正常邮件和垃圾邮件数目
        self.trashnum = 0                                           #初始为史料库中的统计
                                                                    #随着接收邮件的判断，其值还会变动
    #读入字典，默认是当前目录的words.txt，也可自己传入位置参数
    def init_wordslist(self, fn=r"./words.txt"):
        f = open(fn)
        lines = sorted(f.readlines())
        f.close()
        return lines

    #字典树原理可以看这里
    #http://my.oschina.net/u/158589/blog/61037
    def words_2_trie(self, wordslist):
        d = {}
        for word in wordslist:
            ref = d
            chars = self.regex.findall(word)
            for char in chars:
                ref[char] = ref.has_key(char) and ref[char] or {}
                ref = ref[char]

        return d

    def search_in_trie(self, chars, trie, res):
        '''
        逐字检索已经拆分为英文单词或单个汉字的邮件并在字典中查找最长匹配的词语
        '''
        ref = trie
        index = 0
        temp = ''
        count = 0
        for char in chars:
            if ref.has_key(char):
                temp += char
                count += 1
                ref = ref[char]
                index += 1
            else:
                if temp != 0:                                #表示上一个单词已经分离出
                    res.append(temp)
                    temp = ''
                    count = 0
                if index == 0:                               #字典中没有以上一个char结尾的单词
                    index = 1
                    res.append(char)
                try:
                    chars = chars[index:]
                    self.search_in_trie(chars, trie, res)
                except:
                    pass
                break
        if count != 0:                                       #最后一个词
            res.append(temp);
       

    def getNTRatio(self, typ):
        '''
        分别计算正常(Normal)邮件和垃圾(Trash)邮件中某词在其邮件总数的比例
        typ:['normal', 'trash']
        '''
        counter = collections.Counter(self.wordlist[typ])
        dic = collections.defaultdict(list)
        for word in list(counter):
            dic[word].append(counter[word])
        mailcount = len(self.maildic[typ])
        if typ == 'normal':
            self.normalnum = mailcount
        elif typ == 'trash':
            self.trashnum = mailcount
        for key in dic:
            dic[key][0] = dic[key][0] * 1.0 / mailcount
        return dic

    def getRatio(self):
        '''
        计算出所有邮件中包含某个词的比例(比如说10封邮件中有5封包含'我们'这个词，
        那么'我们'这个词出现的频率就是50%，这个词来自所有邮件的分词结果)
        '''
        dic_normal_ratio = self.getNTRatio('normal')                        #单词在正常邮件中出现的概率
        dic_trash_ratio = self.getNTRatio('trash')                          #单词在垃圾邮件中出现的概率
        dic_ratio = dic_normal_ratio
        for key in dic_trash_ratio:
            if key in dic_ratio:
                dic_ratio[key].append(dic_trash_ratio[key][0])
            else:
                dic_ratio[key].append(0.01)                                 #若某单词只出现在正常邮件或垃圾邮件中
                dic_ratio[key].append(dic_trash_ratio[key][0])              #那么我们假定它在没出现类型中的概率为0.01
        for key in dic_ratio:
            if len(dic_ratio[key]) == 1:
                dic_ratio[key].append(0.01)
        return dic_ratio

    def readEmail(self, fn):
        '''
        读取邮件并提取英文单词和汉字
        fn: 文件位置
        返回英文单词和单个汉字组成的list
        '''
        if os.path.exists(fn):
            content = open(fn).read();
            content = content[content.index("\n\n")+2::]                    #去除头信息
            try:
                string = content.decode('utf-8')
                #string = content.decode('gb2312').encode('utf-8')
            except:
                string = content.decode('gb2312', 'ignore')
                #string = content
            chars = self.regex.findall(string.encode('utf-8'))              #chars为英文单词或单个汉字组成了list
            #chars = self.regex.findall(string) 
            return chars


    def splitsingle(self, trie, email):
        '''
        分割单个邮件
        返回分词后的单词列表list
        '''
        try:
            string = email.decode('gbk').encode('utf-8')
        except Exception:
            string = email
        chars = self.regex.findall(string)
        res = []
        self.search_in_trie(chars, trie, res)
        res = list(set(res))
        return res


    def split(self, trie, dirs):
        '''
        dirs: 邮件史料库目录
        '''
        for base_d in dirs:
            for dirt in os.listdir(base_d):
                d = base_d + dirt + "/"
                print d
                for fn in os.listdir(d):
                    res = []
                    fn = d + fn
                    chars = self.readEmail(fn)
                    self.search_in_trie(chars, trie, res)
                    res = list(set(res))
                    self.wordlist[dirt].extend(res)
                    if fn not in self.maildic[dirt]:                           #去重并把每封邮件的分词结果存入字典
                        self.maildic[dirt][fn] = res                           #self.maildic[normal|trash][filename]为该邮件的分词结果集

    def splitByjieba(self, trie, dirs):
        '''
        也可以使用用第三方扩展库结巴中文分词进行分词
        此处提供了调用接口
        '''
        try:
            import jieba
            for base_d in dirs:
                for dirt in os.listdir(base_d):
                    d = base_d + dirt + "/"
                    print d
                    for fn in os.listdir(d):
                        res = []
                        fn = d + fn
                        email = open(fn).read();
                        email = email[email.index("\n\n")::]
                        res = list(jieba.cut(email))
                        res = list(set(res))
                        self.wordlist[dirt].extend(res)
                        if fn not in self.maildic[dirt]:                           #去重并把每封邮件的分词结果存入字典
                            self.maildic[dirt][fn] = res
        except:
            self.split(trie, dirs)

    '''
    服务器每判定一个新邮件都会将结果加到动态数据库中
    typ = 'nomal' | 'trash'
    res is [] 新邮件的分词结果
    '''
    def flush(self, typ, res):
        if typ == 'nomal':
            for word in res:
                if self.ratio[word][0] == 0.01:
                    self.ratio[word][0] = 1.0 / (self.normalnum + 1)
                else:
                    self.ratio[word][0] = (1 + self.ratio[word][0] * self.normalnum) / (self.normalnum + 1)
            self.normalnum += 1
        else:
            for word in res:
                if self.ratio[word][1] == 0.01:
                    self.ratio[word][1] = 1.0 / (self.trashnum + 1)
                else:
                    self.ratio[word][1] = (1 + self.ratio[word][1] * self.trashnum) / (self.trashnum + 1)
                self.trashnum += 1

def main():
    demo  = SplitEmail()
    words = demo.init_wordslist()
    trie  = demo.words_2_trie(words)
    demo.split(trie, ['./data/'])
    #demo.splitByjieba(trie, ['./data/'])
    dic_of_ratio = demo.getRatio()
    ratio = open('ratio.txt', 'w')
    for key in dic_of_ratio:
        try:
            #print key, dic_of_ratio[key]
            #这里真够麻烦的 必须转成gb2312才能在txt里正常显示 XD
            ratio.write(key.decode('utf-8').encode('gb2312'))
            for v in dic_of_ratio[key]:
                 ratio.write(' ' + str(v))
            ratio.write('\n')
        except:
            pass
    ratio.close()
if __name__=='__main__':
    main()
