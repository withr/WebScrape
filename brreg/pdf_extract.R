library(pdftools)
txt <- pdf_text("20170000674504-1.pdf")


nr <- regmatches(txt[1], regexec("Organisasjonsnr:([ 0-9]*)", txt[1]))[[1]][2]
nr <- gsub(" ", "", nr)
