FROM r-base:latest

RUN R -e "install.packages('plumber')" &&  R -e "install.packages('forestplot')"

WORKDIR /app

COPY . /app


CMD ["Rscript", "/app/bootstrap_plumber.R"]
