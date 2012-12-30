# -*- coding: utf-8 -*-
import splitEmail
ps = 0.5													#收到一封新邮件，是垃圾邮件的概率
ph = 0.5                            						# 正常邮件的概率均为50%
															#s: 垃圾邮件
															#h: 正常邮件
															#p: 概率
class JudgeMail:
    '''
    判断接收到的邮件是否为垃圾邮件
    '''
    def judge(self, init, trie, email):
        res = init.splitsingle(trie, email)                  #res是分词结果，为list
        for i in [';', '', ' ', ':', '.', '。', '：', '，', ' ', '!', '（', '）', '(', ')','！','、']:
            if i in res:
                res.remove(i)                                #剔除标点字符
        ratio_of_words = []									 #记录邮件中每个词在垃圾邮件史料库(init.ratio[key][1])中出现的概率	
        for word in res:
            if word in init.ratio:
                ratio_of_words.append((word, init.ratio[word][1]))					 #添加(word, ratio)元祖
            else:
                init.ratio[word] = [0.6, 0.4]				 #如果邮件中的词是第一次出现，那么就假定
                                                             #p(s|w)=0.4	
            ratio_of_words.append((word, 0.4))
        ratio_of_words = sorted(ratio_of_words, key = lambda x:x[1], reverse=True)[:15]
        P = 1.0 
        rest_P = 1.0
        for word in ratio_of_words:
            try:
                print word[0].decode('utf-8'), word[1]
            except:
                print word[0], word[1]
            P *= word[1]
            rest_P = rest_P * (1.0 - word[1])
         
        trash_p = P / (P + rest_P)
        typ = ''
        if trash_p > 0.9:
            typ = 'trash' 
        else:
            typ = 'normal'
        init.flush(typ, res)
        return trash_p