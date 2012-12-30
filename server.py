# -*- coding: utf-8 -*-
import socket
import analysisEmail
import splitEmail

if __name__ == '__main__':
    #加载历史邮件资料库，即建立判断条件
    init = splitEmail.SplitEmail()
    words = init.init_wordslist()
    trie = init.words_2_trie(words)
    init.split(trie, ['./data/'])
    init.ratio = init.getRatio()
    #for key in dic_of_ratio:
    #    print key, dic_of_ratio[key]
    ####################################################################

    host = ''   		# Symbolic name meaning all available interfaces
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    while True:
        print "Waiting for clients..."
        conn, addr = s.accept()
        print 'Connected by', addr
        msg = ""
        while True:
            data = conn.recv(1024)
            if not len(data):
                break
            msg += data
        conn.close()
        P = analysisEmail.JudgeMail().judge(init, trie, msg)
        print "P(spam) = ", P

