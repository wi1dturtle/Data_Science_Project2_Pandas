from datetime import datetime
from heapq import merge

import pandas as pd

customers=pd.read_csv("data/cleaned/customers_clean.csv")
products=pd.read_csv("data/cleaned/products_clean.csv")
transactions=pd.read_csv("data/cleaned/transactions_clean.csv")

###part A
merged=pd.merge(transactions,customers,how='left',on='customer_id')
# used left because to not lose transactions and each transaction will have its own customer
print(merged.columns)
# print(merged.isna().sum()) # no na-s


merged=pd.merge(merged,products,how='left',on='product_id')
# used left for the same reason as before
print(merged)

print(merged.isna().sum()) #
print(merged[merged.isna().any(axis=1)]) # we have unmatched transactions because while
                                        # cleaning products.csv some product_ids were deleted

#since we use left join rows of transactions and merged should be same
print(f"does it has expected rows? {len(transactions)==len(merged)}") #verified so we haven't
                                                                        # lost data

###part B feature engineering
merged.dropna() # to drop all transactions with unexisting prodducts

#financial features
merged.insert(len(merged.columns),'total_amount',merged['price']*merged['quantity'])
merged.insert(len(merged.columns),'discount',merged['total_amount']*merged['quantity'].apply(lambda x: 0.1 if x>3 else 0))
merged.insert(len(merged.columns),'final_amount',merged['total_amount']-merged['discount'])
print(merged[['quantity','total_amount','discount','final_amount']])

#temporal features
merged['transaction_date']=pd.to_datetime(merged['transaction_date'])
merged['registration_date']=pd.to_datetime(merged['registration_date'])

merged.insert(len(merged.columns),'transaction_month',merged['transaction_date'].dt.month)
merged.insert(len(merged.columns),'transaction_day_of_week',merged['transaction_date'].dt.day_name())
merged.insert(len(merged.columns),'customer_age_at_purchase',
              merged['age'] + (
                      (merged['transaction_date'] - merged['registration_date']).dt.days / 365
              ).astype('int'))

print(merged[['customer_age_at_purchase']])

#categorical features

merged['customer_segment']=merged['customer_id'].map(
    merged.groupby('customer_id')['final_amount'].sum().apply(
                  lambda x: "High" if x>1000
                  else "Medium" if 500<=x<=1000
                  else "Low"
              ))
print(merged[['customer_segment']])

merged.insert(len(merged.columns),'age_group',merged['age'].apply(
    lambda x : "18-30" if 18 <= x <= 30
    else "31-45" if 31 <= x <= 45
    else "46-60" if 46 <= x <=60
    else "61+"))
print(merged[['age_group','age']])

merged.insert(len(merged.columns),'is_weekend',merged['transaction_day_of_week'].apply(
    lambda x : True if x=="Saturday" or x=="Sunday" else False))

###Part C Advanced Analysis

#revenue analysis
revenue_by_category = merged.groupby('category')['final_amount'].sum()
print(revenue_by_category)

monthly_revenue = merged.groupby('transaction_month')['final_amount'].sum()
print(monthly_revenue)

revenue_by_country = merged.groupby('country')['final_amount'].sum().sort_values(ascending=False).head(5)
print(revenue_by_country)

avg_transaction_value = merged.groupby('payment_method')['final_amount'].mean()
print(avg_transaction_value)

#customer behaviour
purchases_per_customer = merged.groupby('customer_id').size().sort_values(ascending=False).head(10)
print(purchases_per_customer)

avg_spending_by_age_group = merged.groupby('age_group')['final_amount'].mean()
print(avg_spending_by_age_group)

popular_category_by_country = merged.groupby(['country','category'])['quantity'].sum().reset_index()
popular_category_by_country = popular_category_by_country.sort_values(['country','quantity'], ascending=[True,False]).groupby('country').first()
print(popular_category_by_country)

weekend_vs_weekday = merged.groupby('is_weekend').size()
print(weekend_vs_weekday)
#product performance
top_products_revenue = merged.groupby('product_name')['final_amount'].sum().sort_values(ascending=False).head(10)
print(top_products_revenue)

top_products_quantity = merged.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10)
print(top_products_quantity)

avg_transaction_by_category = merged.groupby('category')['final_amount'].mean().sort_values(ascending=False)
print(avg_transaction_by_category.head(1))

worst_products_revenue = merged.groupby('product_name')['final_amount'].sum().sort_values().head(5)
print(worst_products_revenue)

#summary
pivot_category_country = merged.pivot_table(
    values='final_amount',
    index='category',
    columns='country',
    aggfunc='sum',
    fill_value=0
)

print(pivot_category_country)

cross_age_segment = pd.crosstab(
    merged['age_group'],
    merged['customer_segment'],
    values=merged['final_amount'],
    aggfunc='sum',
    margins=True
)

print(cross_age_segment)

summary = merged.groupby(['country', 'category']).agg(
    total_revenue=('final_amount','sum'),
    avg_transaction=('final_amount','mean'),
    total_quantity=('quantity','sum'),
    transactions=('transaction_id','count')
).reset_index()

print(summary)