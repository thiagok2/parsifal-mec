library(plumber)
r <- plumb("/app/plumber.R")
r$run(host='0.0.0.0',port=8000)
