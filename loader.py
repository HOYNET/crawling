import pandas as pd
import chardet
import yfinance as yf
import logging

# Intercept Error message
class InterceptHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        if "Failed downloads:" in log_message:
            raise Exception("Failed downloads detected: " + log_message)
       

class NasdaqTickerLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def detect_encoding(self):
        with open(self.file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    def load_tickers(self):
        encoding = self.detect_encoding()
        nasdaq_list = pd.read_csv(self.file_path, usecols=[1], encoding=encoding)   # There must be stock codes in the second column, Or manually change codes
        return nasdaq_list.iloc[:, 0].tolist()
    
class NAS_StockDownloader:

    def __init__(self, ticker_list, output_csv, start, end):
        self.ticker_list = ticker_list
        self.output_csv = output_csv
        self.start = start
        self.end = end
        self.total_stock = pd.DataFrame()
        self.exception_stock = pd.DataFrame()

    def download_stock(self, ticker_code):
        
        try:
            indv_stock = yf.download(ticker_code, start=self.start, end=self.end)
            indv_stock['tck_iem_cd'] = ticker_code

            # ticker_code migration to 2nd row
            cols = indv_stock.columns.tolist()
            cols.insert(0, cols.pop(cols.index('tck_iem_cd')))
            indv_stock = indv_stock[cols]

            # remove volume row
            indv_stock.drop('Adj Close', axis=1, inplace=True)

        except Exception as e:
            print(f"Failed to download data for {ticker_code} from {self.start}. Trying from stock's start date.")
            ticker_info = yf.Ticker(ticker_code).info
            
            if 'startDate' in ticker_info:
                start_date = ticker_info['startDate']
                formatted_start_date = pd.Timestamp(start_date, unit='s').strftime('%Y-%m-%d')
                indv_stock = yf.download(ticker_code, start=formatted_start_date, end=self.end)
                indv_stock['tck_iem_cd'] = ticker_code

                # ticker_code migration to 2nd row
                cols = indv_stock.columns.tolist()
                cols.insert(0, cols.pop(cols.index('tck_iem_cd')))
                indv_stock = indv_stock[cols]

                # remove volume row
                indv_stock.drop('Adj close', axis=1, inplace=True)
                self.exception_stock = pd.concat([self.exception_stock, indv_stock])
            else:
                print(f"Failed to retrieve start date for {ticker_code}. Skipping.")
                return None

        return indv_stock

    def execute(self):
        for ticker_code in self.ticker_list:
            stock_data = self.download_stock(ticker_code)
            if stock_data is not None:
                self.total_stock = pd.concat([self.total_stock, stock_data])

    def save_to_csv(self, output_csv, exception_filename='exception_stock_data.csv'):
        self.total_stock.to_csv(output_csv)
        self.exception_stock.to_csv(exception_filename)


