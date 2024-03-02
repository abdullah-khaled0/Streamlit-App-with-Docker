import streamlit as st
import pandas as pd
import plotly.express as px
from functions import fetch_gold_prices, fetch_dollar_prices



docker_path = "docker.png"
streamlit_path = "streamlit.png"

# displaying images side by side
col1, col2 = st.columns(2)

col1.image(docker_path, width=300)
col2.image(streamlit_path, width=300)



st.title('أسعار الذهب والدولار')


gold_info = fetch_gold_prices()

if gold_info is not None and gold_info:
    st.subheader('أسعار الذهب:')

    gold_df = pd.DataFrame(gold_info.items(), columns=['نوع الذهب', 'القيم'])[:-1]

    st.sidebar.title('فلتر الداتا')
    category = st.sidebar.selectbox('حدد العيار', ['الكل'] + list(gold_df['نوع الذهب']))

    filtered_data = gold_df if category == 'الكل' else gold_df[gold_df['نوع الذهب'] == category]

    prices_sell = []
    prices_buy = []
    price_changes = []

    # Extract values from the provided data
    for item in filtered_data["القيم"]:
        prices_sell.append(item.get('سعر البيع', 'N/A'))
        prices_buy.append(item.get('سعر الشراء', 'N/A'))
        price_changes.append(item.get('تغيير السعر', 'N/A'))

    filtered_data = pd.DataFrame({
        "نوع الذهب": filtered_data["نوع الذهب"],
        "سعر البيع": prices_sell,
        "سعر الشراء": prices_buy,
        "تغيير السعر": price_changes
    })

    if not filtered_data.empty:
        st.write(filtered_data)

        # Data visualization - Price Change
        price_change_chart = px.bar(filtered_data, x='نوع الذهب', y='تغيير السعر',
                                    labels={'x': 'نوع الذهب', 'y': 'تغيير السعر'},
                                    title='التغيير في أسعار الذهب')
        st.plotly_chart(price_change_chart, use_container_width=True)
    else:
        st.warning("لا توجد بيانات متاحة للفئة المحددة.")

# Displaying dollar information
dollar_in_bank = pd.DataFrame(gold_info.items(), columns=['نوع الذهب', 'القيم']).iloc[-1]
dollar_in_bank.rename({'نوع الذهب': 'المكان'}, inplace=True)

dollar_place = dollar_in_bank['المكان']
dollar_values = dollar_in_bank['القيم']

data = {
    "العملة": ["سعر البيع", "سعر الشراء", "تغيير السعر"],
    "القيمة": [dollar_values['سعر البيع'], dollar_values['سعر الشراء'], dollar_values['تغيير السعر']]
}

st.subheader('سعر الدولار في البنك المركزي:')
df = pd.DataFrame(data)
st.table(df)

st.subheader('سعر الدولار في السوق السوداء:')
dollar_info = fetch_dollar_prices()



if st.button("تحديث البيانات"):
    pass