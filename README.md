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
> 2. Make sure that the ticker_codes are in the 2nd column of the csv file<br>

대회에서 주어진 NASDAQ_FC_STK_IEM_IFO.csv 파일의 일부분만 깃허브에 등재되었습니다.<br>
추가적인 데이터 수집이 필요한 경우 수집을 하고 싶은 ticker_code들을 csv파일안에 추가 해주시면 됩니다<br>

|isin_cd|tck_iem_cd|...|...|
|---|---|---|---|
|US00211V1061|AACG|...|...|
|...|...|...|...|


## Activation

Set the start_date and end_date of the Crawling in the main.py<br>
Set the kospi_ticker_code for which the data you are searching for<br><br>
📌 If the Crawling resoucre runs out during the process, manually change the ticker code csv file<br>
📌크롤링 리소스 부족으로 인해 전체 ticker_code에 대해 데이터 수집이 안될 경우<br>csv파일의 ticker_code를 나눠서 진행해주세요

```
    python main.py
```

