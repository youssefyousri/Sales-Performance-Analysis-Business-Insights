import pandas as pd
import numpy as np

df = pd.read_csv('File Date/Sales_Data.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print(df.head())
print('*' * 50)
print(df.shape)
print('*' * 50)
print(df.info())
print('*' * 50)
print(df.isnull().sum())
print('*' * 50)
print(df.describe().T)

df.columns = df.columns.str.strip().str.replace(' ', '_').str.capitalize()
print(df.head())

df = df.rename(columns={'Product_category': 'Category'})
df = df.rename(columns={'Cost': 'Total_cost'})


Text_columns = ['Order_id', 'Sales_date', 'Sales_rep', 'Region', 'Category',
                'Product', 'Customer_type', 'Payment_method', 'Sales_channel']

for i in Text_columns:
    df[i] = df[i].astype(str).str.strip()
    df[i] = df[i].replace(('', 'NAN', 'Nan', 'nan'), np.nan)
    df[i] = df[i].str.title()
print(df.head())

df['Sales_date'] = pd.to_datetime(df['Sales_date'], errors='coerce')

df['Year_date'] = df['Sales_date'].dt.year
df['month_date'] = df['Sales_date'].dt.to_period('M')


df['Sales_rep'] = df['Sales_rep'].fillna(df['Sales_rep'].mode()[0])
df['Region'] = df['Region'].fillna(df['Region'].mode()[0])
df['Payment_method'] = df['Payment_method'].fillna(
    df['Payment_method'].mode()[0])
df['Customer_type'] = df['Customer_type'].fillna(df['Customer_type'].mode()[0])
df['Category'] = df['Category'].fillna(df['Category'].mode()[0])

df['Total_sales'] = df['Unit_price'] * df['Quantity']
df['Total_profit'] = df['Total_sales'] - df['Total_cost']
print(df.head())


# ==========================================
# 1. Overview Page Analysis
# ==========================================
# KPIs Analysis
Total_Sales = df['Total_sales'].sum()
print(round(Total_Sales, 2))

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)

Total_vip_Customer = (df['Customer_type'] == 'Vip').sum()
print(Total_vip_Customer)

Profit_margin = (df['Total_profit'].sum() / Total_Sales)*100
print(round(Profit_margin, 2))


Revenue_Trend = df.groupby('Year_date').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Revenue_Trend)


Sales_Channel_Analysis = df.groupby('Sales_channel').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Sales_Channel_Analysis)


Customer_Segments = df.groupby(
    ['Customer_type']).size().reset_index(name='Total_orders')
print(Customer_Segments)


Region_Analysis = df.groupby('Region').agg(
    Total_Sales=('Total_sales', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Region_Analysis)


Top_Product = df.groupby('Product').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
    Total_Profit=('Total_profit', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Top_Product.head(5))


Sales_Rep_Analysis = df.groupby('Sales_rep').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Top_Product)


# ==========================================
# 2. Revenue Page Analysis
# ==========================================
# KPIs Analysis
Total_Profit = df['Total_profit'].sum()
print(round(Total_Profit, 2))

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)

Profit_margin = (df['Total_profit'].sum() / Total_Sales)*100
print(round(Profit_margin, 2))


Revenue_Trend = df.groupby('Year_date').agg(
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Profit', ascending=False).reset_index()
print(Revenue_Trend)


Sales_Channel_Analysis = df.groupby('Sales_channel').agg(
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Profit', ascending=False).reset_index()
print(Sales_Channel_Analysis)


Customer_Segments = df.groupby('Customer_type').agg(
    Total_Profit=('Total_profit', 'sum')
).sort_values('Total_Profit', ascending=False).reset_index()
print(Customer_Segments)


Region_Analysis = df.groupby('Region').agg(
    Total_Profit=('Total_profit', 'sum')
).sort_values('Total_Profit', ascending=False).reset_index()
print(Region_Analysis)


Top_Product = df.groupby('Product').agg(
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
    Total_Cost=('Total_cost', 'sum')
).sort_values('Total_Profit', ascending=False).reset_index()
print(Top_Product.head(5))


Sales_rep_Analysis = df.groupby('Sales_rep').agg(
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
).sort_values('Total_Profit', ascending=False).reset_index()
print(Sales_rep_Analysis)


# ==========================================
# 3. Customer Page Analysis
# ==========================================
# KPIs Analysis
Total_Customer_orders = (df['Customer_type']).count()
print(Total_Customer_orders)

New_Customer_Orders = (df['Customer_type'] == 'New').sum()
print(New_Customer_Orders)

Returning_Customer_Orders = (df['Customer_type'] == 'Returning').sum()
print(Returning_Customer_Orders)

Returing_Rate_Orders = round(
    (Returning_Customer_Orders / Total_Customer_orders) * 100.0, 2)
print(Returing_Rate_Orders)


Customer_growth_over_time = df.groupby(['Year_date', 'Customer_type']
                                       ).size().reset_index(name='Customer_Count')
print(Customer_growth_over_time)


Customer_Segments = df.groupby(
    ['Customer_type']).size().reset_index(name='Customer_Count')
print(Customer_Segments)


Revenue_by_Customer = df.groupby('Customer_type').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
).sort_values('Total_Sales', ascending=False).reset_index()
print(Revenue_by_Customer)


Customer_Location = df.groupby(
    ['Region', 'Customer_type']).size().reset_index(name='Customer_Count')
print(Customer_Location)


# ==========================================
# 4. Product Page Analysis
# ==========================================
# KPIs
Total_Product = df['Product'].nunique()
print(Total_Product)

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)


Product_over_time = df.groupby(['Year_date', 'Product']
                               )['Quantity'].sum().reset_index(name='Total_Quantity')
print(Product_over_time)


Gategory_Segments = df.groupby(
    ['Category']).size().reset_index(name='Total_Orders')
print(Gategory_Segments)


Product_by_Region = df.groupby(['Region', 'Product'])[
    'Quantity'].sum().reset_index(name='Total_Quantity')
print(Product_by_Region)


Revenue_by_Product = df.groupby('Product').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_Sales', ascending=False).reset_index()
print(Revenue_by_Product)


# ==========================================
# 5. Sales Rep Page Analysis
# ==========================================
# KPIS
Total_Sales_rep = df['Sales_rep'].nunique()
print(Total_Sales_rep)

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)


Sales_rep_over_time = df.groupby(['Year_date', 'Sales_rep']
                                 )['Total_sales'].sum().reset_index(name='Total_quantity')
print(Sales_rep_over_time)


Sales_rep_analysis = df.groupby('Sales_rep').agg(
    Total_sales=("Total_sales", 'sum'),
    Total_Profit=('Total_profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).sort_values('Total_sales', ascending=False).reset_index()
print(Sales_rep_analysis)


Sales_rep_Orders = df.groupby(
    ['Sales_rep']).size().reset_index(name='Total_Orders')
print(Sales_rep_Orders)


Sales_rep_by_Region = df.groupby(['Sales_rep', 'Region'])[
    'Quantity'].sum().reset_index(name='Total_Quantity')
print(Sales_rep_by_Region)


# ==========================================
# 6. Channel Page Analysis
# ==========================================
# # KPIs
Total_Channel = df['Sales_channel'].nunique()
print(Total_Channel)

Total_Quantity = df['Quantity'].sum()
print(Total_Quantity)


Channel_over_time = df.groupby(['Year_date', 'Sales_channel']
                               )['Quantity'].sum().reset_index(name='Total_Quantity')
print(Channel_over_time)


Channel_Analysis = df.groupby(
    ['Sales_channel']).size().reset_index(name='Total_Orders')
print(Channel_Analysis)


Channel_by_Region = df.groupby(['Sales_channel', 'Region']
                               ).size().reset_index(name='Total_Orders')
print(Channel_by_Region)


Channel_by_Product = df.groupby('Sales_channel').agg(
    Total_Sales=('Total_sales', 'sum'),
    Total_Quantity=('Quantity', 'sum'),
).sort_values('Total_Sales', ascending=False).reset_index()
print(Channel_by_Product)


df.to_csv('File Date/Sales_Data_Cleaned_2021_2026.csv', index=False)
