# -*- coding: utf-8 -*-
import socket
import analysisEmail
import splitEmail

if __name__ == '__main__':
    #加载历史邮件资料库，即建立判断条件
    init = splitEmail.SplitEmail()
    words = init.init_wordslist()
    trie = init.words_2_trie(words)
    init.splitByjieba(trie, ['./gavindlutsw/'])
    dic_of_ratio = init.getRatio()
    #for key in dic_of_ratio:
    #    print key, dic_of_ratio[key]
    ####################################################################

    host = ''   		# Symbolic name meaning all available interfaces
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    msg = ""
    while 1:
        data = conn.recv(1024)
        if not len(data):
            break
        msg += data
    #print msg
    conn.close()
    P = analysisEmail.JudgeMail().judge(init, dic_of_ratio, trie, msg)
    print P
