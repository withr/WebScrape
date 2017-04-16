library(rvest)

Nr_ls <- read.csv("orgnummer til tian.txt")
Nr_ls$Content <- NA

URL = "https://w2.brreg.no/enhet/sok/detalj.jsp;jsessionid=PB1RWbF1Ufm2Z-MK8oLoN36f-g0cPl7xPpnF7kjupi2dkbTXzb67!1510308257?orgnr="
for (i in 1:nrow(Nr_ls)) {
    print(i)
    nr  <- Nr_ls$Organisasjonsnummer[i]
    url <- paste(URL, nr, sep = "")
    src <- read_html(url)
    tab_lft <- src %>% html_nodes("div .row")  %>% html_nodes("div .col-sm-4") 
    tab_rgt <- src %>% html_nodes("div .row")  %>% html_nodes("div .col-sm-8") 
    id = grep("Organisasjonsform", tab_lft)
    tg = tab_rgt[id]
    txt = tg %>% html_text()
    Nr_ls$Content[i] <- gsub("\n *", "", txt)
    Sys.sleep(1)
}

write.table(Nr_ls, "Organisasjonsform.txt", sep = ";", row.names = FALSE)
