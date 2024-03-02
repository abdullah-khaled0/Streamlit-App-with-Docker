import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd


# fetch data from the website
def fetch_gold_prices():
    url = "https://market.isagha.com/prices"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        gold_info = {}
        for panel in soup.find_all(class_='isagha-panel'):
            carat = panel.find(class_='gauge').get_text(strip=True)
            selling_price = panel.find_all(class_='value')[0].get_text(strip=True)
            buying_price = panel.find_all(class_='value')[1].get_text(strip=True)
            price_change = panel.find_all(class_='value')[2].get_text(strip=True)

            gold_info[carat] = {
                'سعر البيع': selling_price,
                'سعر الشراء': buying_price,
                'تغيير السعر': price_change,
            }
        return gold_info
    else:
        st.error("فشل في استرداد صفحة الويب.")
        return None
    

def fetch_dollar_prices():
    url = "https://egcurrency.com/ar/currency/egp/exchange"
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', class_='table-hover')

        dollar_buying_rates = []
        dollar_selling_rates = []

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 3:
                currency = cells[0].text.strip()
                # Check if the currency is US Dollar
                if currency.startswith('دولار أمريكى'):
                    buying_rate = cells[1].text.strip()
                    selling_rate = cells[2].text.strip()
                    dollar_buying_rates.append(buying_rate)
                    dollar_selling_rates.append(selling_rate)

        # Create a DataFrame
        df = pd.DataFrame({
            'سعر الشراء': dollar_buying_rates,
            'سعر البيع': dollar_selling_rates
        })

        st.write(df)
    else:
        print("Failed to retrieve the webpage.")
