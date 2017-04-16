library(rvest)


src <- read_html("Bestilling av utskrifter, attester og kopier - Brønnøysundregistrene.htm")

tab <- src %>% html_nodes("table") 
Dat <- tab[8] %>% html_nodes("tr")
dat <- data.frame(id = NA, link = NA, PDF = NA)

for (i in 1:length(Dat)) {
    tmp <- Dat[i]
    N <- grep("Årsregnskap", tmp)
    if (length(N) > 0) {
        print(i)
        id_ <- tmp %>% html_nodes("td")
        id  <- id_[3] %>% html_text()
        yr  <- id_[1] %>% html_text()
        link <- tmp %>% html_node("a") %>% html_attr('href')
        download.file(link, destfile = paste(id, " ", yr, ".pdf", sep = ""))
    }
}



list.files(pattern = ".pdf")
