# plumber.R

#* parse JSON
#* @serializer contentType list(type="image/svg+xml")
#* @get /forestplot
#* @post /forestplot
function(studies, efs) {
 library(forestplot)
  mn <- c(NA, NA)
  lw <- c(NA, NA)
  up <- c(NA, NA)
  mn_names <- c("", "Effect size")
  st_names <- c("", "Estudo")

  names <- as.vector(unlist(studies[1]))
  means <- as.vector(unlist(studies[2]))
  lowers <- as.vector(unlist(studies[3]))
  uppers <- as.vector(unlist(studies[4]))

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

  st_names <- c(st_names, NA, "Sumarização")
  mn_names <- c(mn_names, NA, efs$mean)

  cochrane_from_rmeta <-
  structure(list(
    mean  = mn, 
    lower = lw,
    upper = up),
    .Names = c("mean", "lower", "upper"), 
    row.names = c(NA, -11L), 
    class = "data.frame")

  tabletext<-cbind(
  st_names,
  mn_names)    
  
  tmp <- tempfile()
  svg(tmp)

  forestplot(tabletext, 
           hrzl_lines = list("3" = gpar(lty=2), 
                             "11" = gpar(lwd=1, columns=1:2, col = "#000044")),
           cochrane_from_rmeta,new_page = TRUE,
           is.summary=c(TRUE,TRUE,rep(FALSE,8),TRUE),
           clip=c(0.1,2.5), 
           xlog=TRUE, 
           col=fpColors(box="royalblue",line="darkblue", summary="royalblue"))

  dev.off()

  readBin(tmp, "raw", n=file.info(tmp)$size)
  
}



