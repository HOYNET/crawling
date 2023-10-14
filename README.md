## Prerequisites

* install conda
* create a new conda environment
```
     conda env create -f environment.yml && conda activate crawling
```

* install extra requirements
```
    pip install pykrx yfinance
```


## Preparing Data for Crawling

> 1. Receive Data for tickers of NASDAQ Stock in the root of the Project as a csv file <br>
> 2. Make sure that the ticker_codes are in the 2nd column of the csv file

|isin_cd|tck_iem_cd|...|...|
|---|---|---|---|
|US00211V1061|AACG|...|...|
|...|...|...|...|


## Activation

Set the start_date and end_date of the Crawling in the main.py<br>
Set the kospi_ticker_code for which the data you are searching for<br>
📌 If the Crawling resoucre runs out during the process, manually change the ticker code csv file

```
    python main.py
```

