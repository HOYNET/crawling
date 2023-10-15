import pandas as pd
import chardet
import yfinance as yf
import logging
import os
from pykrx import stock
from kos import KOS_StockDownloader
from loader import NAS_StockDownloader, NasdaqTickerLoader, InterceptHandler

hoynet_home = './'
nasdaqdata_path = './NASDAQ'
kospidata_path = './KOSPI'
indicator_path = './IND'

### Naming csv files ###

# Input Stock items Information
stock_list = 'NASDAQ_FC_STK_IEM_IFO.csv'

# Data without Indicators
nasdaq_output_file = 'NASDAQ_DATA.csv'
merged_nasdaq_output_file = 'MERGED_NASDAQ_DATA.csv'
kospi_output_file = 'KOSPI_DATA.csv'
kospi_ticker_code = '000020'

# Data with Indicators
ind_nasdaq_output_file = 'E_NASDAQ_DATA.csv'

### ( change the name in this section ) ###

# Assigning Start / End date 

start_date = '2013-01-01'
end_date = '2023-08-31'

def nasdaq_crawl(stock_list, output_csv):

    # loading stock list
    loader = NasdaqTickerLoader(file_path)
    ticker_list = loader.load_tickers()

    # yfinance logger error handling (Failed data)
    logger = logging.getLogger('yfinance')
    logger.setLevel(logging.INFO)
    handler = InterceptHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # download Stock Data
    downloader = NAS_StockDownloader(ticker_list, output_csv, start=start_date, end=end_date)
    downloader.execute()
    downloader.save_to_csv(output_csv, 'exception_stock_data.csv')


def indicator_merge(origianl_csv, merged_csv):

    # uploading origianl data
    merged_stock_data = pd.read_csv(origianl_csv, parse_dates=['Date'])

    # gold_value 100 troy ounce, 10Y_american_bond data, USD/KRW, dow_jonse
    gold_data = yf.download('GC=F', start=start_date, end=end_date)
    bond_data = yf.download('^TNX', start=start_date, end=end_date)
    dow_jones = yf.download("^DJI", start=start_date, end=end_date)

    # change row name
    gold_data.rename(columns={"Open": "gold"}, inplace=True)
    bond_data.rename(columns={"Open": "bond"}, inplace=True)
    dow_jones.rename(columns={"Open": "dow"}, inplace=True)

    # setting rows for matching Date index
    merged_stock_data.set_index('Date', inplace=True)
    gold_data.reset_index(inplace=True)
    bond_data.reset_index(inplace=True)
    dow_jones.reset_index(inplace=True)

    gold_data.set_index('Date', inplace=True)
    bond_data.set_index('Date', inplace=True)
    dow_jones.set_index('Date', inplace=True)    

    # merging with original_stock_data
    merged_stock_data = merged_stock_data.merge(gold_data[['gold']], on='Date', how='left')
    merged_stock_data = merged_stock_data.merge(bond_data[['bond']], on='Date', how='left')
    merged_stock_data = merged_stock_data.merge(dow_jones[['dow']], on='Date', how='left')

    # Replacing NaN's with final_stock_data
    merged_stock_data.fillna(0, inplace=True)

    merged_stock_data.reset_index(inplace=True)
    merged_stock_data.to_csv(merged_csv, index=False)

    gold_path = os.path.join(indicator_path, 'gold_data.csv')    
    bond_path = os.path.join(indicator_path, 'amreican_bond_data.csv')    
    dow_path = os.path.join(indicator_path, 'dow_jones.csv')    
    
    gold_data.to_csv(gold_path)
    bond_data.to_csv(bond_path)
    dow_jones.to_csv(dow_path)

def nasdaq_merge(file_path):

    # csv_name = './NASDAQ/NASDAQ_DATA'
    csv_name = nasdaqdata_path + '/' + nasdaq_output_file[0:len(nasdaq_output_file)-4]
    total_stock = pd.DataFrame()

    for i in range(1,6):

        if i==0:
            continue
        
        elif i==1:
            merge_file = csv_name + '.csv'
        
        else:    
            merge_file = csv_name + str(i) + '.csv'
        ind_stock_data = pd.read_csv(merge_file)
        total_stock = pd.concat([total_stock, ind_stock_data])

    total_stock.to_csv(file_path)


if __name__ == "__main__":
    
    # Making path for Data
    file_path = os.path.join(hoynet_home, stock_list)

    nas_file_path = os.path.join(nasdaqdata_path, nasdaq_output_file)
    ind_nas_file_path = os.path.join(nasdaqdata_path, ind_nasdaq_output_file)
    merged_nas_file_path = os.path.join(nasdaqdata_path, merged_nasdaq_output_file)

    kos_file_path = os.path.join(kospidata_path, kospi_output_file)

    # NASDAQ Crawling implement
    nasdaq_crawl(file_path, nas_file_path)
    indicator_merge(nas_file_path, ind_nas_file_path)

    # KOSPI Crawling implement
    kospi_crawl = KOS_StockDownloader(stock, start_date, end_date)
    kospi_crawl.execute(kospi_ticker_code)
    kospi_crawl.save_data(kos_file_path)

    # NASDAQ Data Merging
    # nasdaq_merge(merged_nas_file_path)

