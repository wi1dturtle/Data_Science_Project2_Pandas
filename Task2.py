from idlelib.pyparse import trans

import pandas as pd

from Task3 import transactions

customers=pd.read_csv("data/original/customers.csv")
customers_org=pd.read_csv("data/original/customers.csv")

products=pd.read_csv("data/original/products.csv")
products_org=pd.read_csv("data/original/products.csv")

transactions=pd.read_csv("data/original/transactions.csv")
transactions_org=pd.read_csv("data/original/transactions.csv")

## part A data quality issues

# customers
print(customers['email'])
print(f"how many missed emails: {customers['email'].isna().sum()}")

print(f"how many duplicates: {customers.duplicated().sum()}")

print(customers.dtypes) # age should be int


print(f"count US: {customers['country'].loc[customers['country']=="US"].count()}")
print(f"count USA: {customers['country'].loc[customers['country']=="USA"].count()}")
print(f"count United States: {customers['country'].loc[customers['country']=="United States"].count()}")

#   products
print(f"how many missed prices: {products['price'].isna().sum()}")

print(f"how many negative emails: {(products['price']<0).sum()}")

print(f"number of stock>1000: {(products['stock']>1000).sum()}") ## we have 3 stock values>1k

print(f"number of prod_names with spaces around: {products['product_name'].str.match(r'^\s+|\s+$').sum()}")

print(products['category'].drop_duplicates()) # there is sports and Sports, Home and home...

# transactions
print(transactions.columns)

print(f"rows where quantities are nan:\n{transactions.loc[transactions['quantity'].isna()]}")

print(f"rows where transactions duplicate:\n{transactions.loc[transactions['transaction_id'].duplicated()]}")

print(transactions['customer_id'].isna().sum()) # 0 nan elements, IDK whan invalid meant in problem

print(transactions.loc[pd.to_datetime(transactions['transaction_date'])>pd.Timestamp.now()])

print(transactions['payment_method'].drop_duplicates()) # we have PayPal and PAYPAL and so on


##part B data cleaning

#handle missing values

customers=customers.dropna(subset=['email']) #mail nan rows droped

# print(transactions.columns)

products['price']=products['price'].fillna(products.groupby('category')['price'].
                                           transform('median'))  # price nan replaced with median

transactions['quantity']=(transactions['quantity'].fillna(transactions['quantity'].mode()[0]))
# replace all Nan quantitys with first mode element

#remove duplicates

print(customers.duplicated().sum()) # we have 4 duplicated rows
customers=customers.drop_duplicates(keep='first')

print(products.duplicated().sum()) # we have 0 duplicated rows
products=products.drop_duplicates(keep='first') # but still remove duplicates

print(transactions.duplicated().sum()) # we have 6 duplicated rows
transactions=transactions.drop_duplicates(keep='first')

# fix data types

customers['age'] = customers['age'].str.extract(r'(\d+)').astype(float).astype('Int64')
print(customers['age'].dtype) #Int64 before it was Object

print(transactions['transaction_date'].dtype) #object
transactions['transaction_date']=pd.to_datetime(transactions['transaction_date'])
print(transactions['transaction_date'].dtype) #datetime64[ns]



print(pd.to_numeric(products['price']))
print(pd.to_numeric(transactions['quantity']))

# standardize values
customers['country'] = customers['country'].replace({
    'US': 'United States',
    'USA': 'United States'
})

customers=customers.drop_duplicates(keep='first') ## since last update may cause duplicates


text_cols = customers.select_dtypes(include='object').columns  # all text columns
customers[text_cols] = customers[text_cols].apply(lambda x: x.str.strip())

text_cols = products.select_dtypes(include='object').columns  # all text columns
products[text_cols] = products[text_cols].apply(lambda x: x.str.strip())

text_cols = transactions.select_dtypes(include='object').columns  # all text columns
transactions[text_cols] = transactions[text_cols].apply(lambda x: x.str.strip())

customers['email']=customers['email'].str.lower()


# handle outliners & invalid data

products=products[products['price']>=0]

products['stock']=products['stock'].apply(lambda x: 500 if x>500 else x)


transactions=transactions[transactions['customer_id'].isin(customers['customer_id'])]
print("###########" , transactions['customer_id']) # i dont know what is invalid in customers_id

transactions=transactions[transactions['transaction_date']<=pd.Timestamp.now()]


##Part C validation
print(f"rows of customers: {len(customers)} , original was 205")
print(f"rows of customers: {len(products)} , original was 50")
print(f"rows of customers: {len(transactions)} , original was 508")

print(f"number of missing values (customers): {customers.isna().sum().sum()}")
print(f"number of missing values (customers_org): {customers_org.isna().sum().sum()}")

print(f"number of missing values (products): {products.isna().sum().sum()}")
print(f"number of missing values (products_org): {products_org.isna().sum().sum()}")

print(f"number of missing values (transactions): {transactions.isna().sum().sum()}")
print(f"number of missing values (transactions_org): {transactions_org.isna().sum().sum()}")

print(f"number of duplicates were (customers): {customers_org.duplicated().sum()} "
      f"and now is: {customers.duplicated().sum()}")
print(f"number of duplicates were (products): {products_org.duplicated().sum()} "
      f"and now is: {products.duplicated().sum()}")
print(f"number of duplicates were (transactions): {transactions_org.duplicated().sum()} "
      f"and now is: {transactions.duplicated().sum()}")

customers['registration_date']=pd.to_datetime(customers['registration_date'])
#not mantion in the task but still converting from object to datetime
print(f"data types of customers:\n{customers.dtypes}")
print(f"data types of products:\n{products.dtypes}")
print(f"data types of transactions:\n{transactions.dtypes}") #everything good

transactions['payment_method']=transactions['payment_method'].replace({
    'PAYPAL' : 'PayPal',
    'CREDIT CARD' : 'Credit Card',
    'BANK TRANSFER' : 'Bank Transfer'
})
products['category']=products['category'].replace({
    'electronics' : 'Electronics',
    'books' : 'Books',
    'home' : 'Home',
    'sports' : 'Sports'
})
#also not mention to fix this but did it

#exporting
customers.to_csv('customers_clean.csv', index=False)
products.to_csv('products_clean.csv', index=False)
#print("#" , transactions['transaction_date'].dtype)
transactions.to_csv('transactions_clean.csv', index=False)











