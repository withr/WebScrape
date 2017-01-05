from bs4 import BeautifulSoup as BS
import time, re, os, pickle, sys

tags = ["shiny", "shinyapps", "shiny-server", "shinydashboard"]
wd = "/home/tian/shinyExpert/StackOverflow/"

topics = []
for tag in tags: 
    path = wd + tag + "/"
    print path
    HTML = os.listdir(path)
    HTML.sort()
    for i in range(0, len(HTML)):
        f = HTML[i]
        bs = BS(open(path + f).read())
        threads = [f]
        try:
            Q = bs.find("div", {"id": "question"})
            Q_text = Q.find("div", {"class": "post-text"})
            q_text = Q_text.get_text()
            Q_time = Q.findAll("div", {"class": "user-action-time"})
            q_time = Q_time[0].find("span")["title"]
            Q_name = Q.findAll("a", {"href": re.compile("/users/.*")})
            q_name = Q_name[len(Q_name)-1].get_text()
            Q_cmnt = Q.findAll("tr", {"class": "comment"})
            cmnts = []
            if (len(Q_cmnt) > 0):
                for c in range(0, len(Q_cmnt)):
                    c_text = Q_cmnt[c].find("span", {"class": "comment-copy"}).get_text()
                    c_name = Q_cmnt[c].find("a", {"href": re.compile("/users/.*")}).get_text()
                    c_time = Q_cmnt[c].find("span", {"class": "relativetime-clean"})["title"]
                    cmnt = {"text": c_text, "name": c_name, "time": c_time}
                    cmnts.append(cmnt)
            threads = [{"text": q_text, "time": q_time, "name": q_name, "comments":cmnts}]
            A = bs.findAll("div", {"class": "answer"})
            for n in range(0, len(A)):
                A_text = A[n].find("div", {"class": "post-text"})
                a_text = A_text.get_text()
                A_time = A[n].findAll("div", {"class": "user-action-time"})
                a_time = A_time[0].find("span")["title"]
                A_name = A[n].findAll("a", {"href": re.compile("/users/.*")})
                a_name = A_name[len(A_name)-1].get_text()
                A_cmnt = A[n].findAll("tr", {"class": "comment"})
                cmnts = []
                if (len(A_cmnt) > 0):
                    for c in range(0, len(A_cmnt)):
                        c_text = A_cmnt[c].find("span", {"class": "comment-copy"}).get_text()
                        c_name = A_cmnt[c].find("a", {"href": re.compile("/users/.*")}).get_text()
                        c_time = A_cmnt[c].find("span", {"class": "relativetime-clean"})["title"]
                        cmnt = {"text": c_text, "name": c_name, "time": c_time}
                        cmnts.append(cmnt)  
                thread = {"text": a_text, "time": a_time, "name": a_name, "comments":cmnts}
                threads.append(thread)
        except:
            with open(wd + 'log_extract.txt', "a") as log:
                log.write(f + "\n")
                log.close()
            print "\nError encountered: " + f
        topics.append(threads)
        msg = "\rProcessed " + str(i+1) + " files: " + f
        sys.stdout.write(msg); sys.stdout.flush()
  

  
dat_topics = wd + "topics.dat"
pickle.dump(topics, open(dat_topics, "wb"))



