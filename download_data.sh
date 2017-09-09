cat data_urls.txt | xargs -n 1 -P 4 wget -P data/
unzip 'data/*.zip' -d data/
