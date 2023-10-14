## Prerequisites

* install conda
* create a new conda environment
```
    conda create --name [your_enviroment_name]
```

* install requirements
```
    pip install pykrx fsspec chardet
    pip install yfinance
```


## Preparing Data for Crawling

> 1. Receive Data for tickers of NASDAQ Stock in the root of the Project as a csv file <br>
> 2. Make sure that the ticker_codes are in the 2nd column of the csv file<br>


## Activate Crawling
```
    python main.py
```

