import pandas as pd

def convert_date(date_str):
    return date_str.replace("-", "")

class KOS_StockDownloader:
        
    def __init__(self, stock, start_date, end_date, market="KOSPI"):
        self.stock = stock
        self.start_date = convert_date(start_date)
        self.end_date = convert_date(end_date)
        self.market = market
        self.df_full = pd.DataFrame()

    def execute(self, start_ticker):
        tickers = self.stock.get_market_ticker_list(self.end_date, market=self.market)
        tickers = sorted(tickers)
        flag=False

        for i in tickers:
            
            if i == start_ticker:
                flag = True

            if flag:    
                try:
                    df = self.stock.get_market_ohlcv_by_date(self.start_date, self.end_date, i)
                    if '등락률' in df.columns:
                        df = df.drop('등락률', axis=1)
                    df['종목명'] = i
                    cols = df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    df = df[cols]
                    self.df_full = pd.concat([self.df_full, df])
                except Exception as e:
                    print(f"Error with ticker {i}: {e}")

    def save_data(self, file_name):
        self.df_full.to_csv(file_name, encoding="utf-8-sig")
