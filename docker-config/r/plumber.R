# plumber.R

#* parse JSON
#* @serializer contentType list(type="image/svg+xml")
#* @get /forestplot
#* @post /forestplot
function(studies, efs, labels) {
 library(forestplot)
  mn <- c(NA, NA)
  lw <- c(NA, NA)
  up <- c(NA, NA)
  mn_names <- c("", labels$efs_label)
  st_names <- c("", labels$study_label)

  names <- as.vector(unlist(studies$name))
  means <- as.vector(unlist(studies$mean))
  lowers <- as.vector(unlist(studies$lower))
  uppers <- as.vector(unlist(studies$upper))

  for(name in names)
    st_names <- c(st_names, name)
  
  for(mean in means) {
    mn <- c(mn, as.numeric(mean))
    mn_names <- c(mn_names, mean)
  }  

  for(lower in lowers)
    lw <- c(lw, as.numeric(lower))

  for(upper in uppers)
    up <- c(up, as.numeric(upper))

  mn <- c(mn, NA, as.numeric(efs$mean))
  lw <- c(lw, NA, as.numeric(efs$lower))
  up <- c(up, NA, as.numeric(efs$upper))

  st_names <- c(st_names, NA, labels$summary_label)
  mn_names <- c(mn_names, NA, efs$mean)

  final_intervalo <- length(up) - 3

  cochrane_meta <- data.frame(
  coef = mn,
  low = lw,
  high = up)


  tabletext<-cbind(
  st_names,
  mn_names)    
  
  tmp <- tempfile()

  svg(tmp)

  forestplot(tabletext,
           hrzl_lines = TRUE, 
           cochrane_meta, new_page = TRUE,
           is.summary=c(FALSE, TRUE, rep(FALSE, final_intervalo), TRUE),
           clip=c(-0.5,1.2), 
           xlog=FALSE,
	   col=fpColors(box="royalblue",line="darkblue", summary="royalblue"))

  dev.off()

  readBin(tmp, "raw", n=file.info(tmp)$size)
  
}



