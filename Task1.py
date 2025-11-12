import pandas as pd


# part A loading data
customers=pd.read_csv("data/original/customers.csv")

products=pd.read_csv("data/original/products.csv")

transactions=pd.read_csv("data/original/transactions.csv")


####
# parb B Data Exploration

def basic_info(df):
    print(f"first five rows:\n{df.head(5)}")
    print(f"last five rows:\n{df.tail(5)}")
    print(f"rows: {len(df)} columns: {len(df.columns)}")
    print(f"column names and types: {df.dtypes}")
    print(f"memory usage:\n{df.memory_usage()}")

#basic_info(customers)

def statistical_summary(df):
    print(df.describe())
    print(df.describe(include='object'))
    for col in df.select_dtypes(include='object').columns:
        print(f"unique values in {col}: {df[col].nunique()}")

#statistical_summary(products)

def data_quality_check(df):
    print(f"missing values per column:\n{df.isnull().sum()}")
    print(f"duplicated rows: {df.duplicated().sum()}")

#data_quality_check(customers)

###
#part C basic analysis

#customer analysis
print(customers.groupby(by='country').size().reset_index(name='customer_count'))

customers['age'] = customers['age'].replace(r'[^0-9]', '', regex=True).astype(float)
print(f"eldest customers age: {customers['age'].max()}\n"
      f"youngest customers age: {customers['age'].min()}\n"
      f"average age of customers: {customers['age'].mean():.2f}\n"
      f"median of customers age: {customers['age'].median()}")

print("month with most registrations: " +
    pd.to_datetime(customers['registration_date']).dt.month_name().value_counts().idxmax())

#product analysis
print(products.groupby(by='category').size())

print(products.groupby(by='category')['price'].mean())

print(products.query('stock == 0'))

#transaction analysis
print(transactions.groupby(by='payment_method').size())

print("most popular product id: " + transactions.groupby(by='product_id').size().idxmax())

print("customer id with most purchases: " + transactions.groupby(by='customer_id').size().idxmax())

####################



