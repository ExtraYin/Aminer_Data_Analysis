#!/bin/bash

# echo "Downloading and unzipping AMiner-Author data......"
# wget -N -O data/raw/AMiner-Author.zip http://doc.argcv.com/AMinerNetwork/AMiner-Author.zip
# unzip data/raw/AMiner-Author.zip -d data/raw

if [ -e x.txt ]
then
    echo "Downloading and unzipping dblp.v10 data......"
	wget -N -O data/raw/dblp.v10.zip https://static.aminer.org/lab-datasets/citation/dblp.v10.zip
else
    echo "dblp.v10.zip already exisits."
fi

unzip data/raw/dblp.v10.zip -d data/raw