import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def importing_data():
    """
    Importing dataset from local directory
    :return:
    """
    data = pd.read_csv('/Users/vishal/Documents/code/supply-chain-orchestration/src/scm-dataset/SupplyChainDataset.csv',
                       header=0, encoding='unicode_escape')
    pd.set_option('display.max_columns', None)
    return data


def extract_shipment_features(data):
    """
    Make a corelation map to extract out shipment features
    :return: panda data frame with shipment features
    """
    shipment_features = ['Type', 'Days for shipping (real)', 'Days for shipment (scheduled)', 'Late_delivery_risk',
                         'Benefit per order',
                         'Sales per customer', 'Latitude', 'Longitude', 'Shipping Mode', 'Order Status', 'Order Region',
                         'Order Country', 'Order City', 'Market', 'Delivery Status']
    shipment = data[shipment_features]
    shipment.head()
    return shipment


def extract_financial_features(data):
    """
    Make a correlation map to extract out financial features
    :param data:
    :return: return financial feature in form of panda dataframe
    """
    finance_features = ['Benefit per order', 'Sales per customer', 'Order Item Discount', 'Order Item Discount Rate',
                        'Order Item Product Price', 'Order Item Profit Ratio']
    finance = data[finance_features]
    finance.head()
    return finance


def data_info(data):
    """
    Exploration of the dataset
    :param data:
    """
    print('1) Number of columns are : ', data.shape[1])
    print('2) Number of rows are : ', data.shape[0])
    print('3) Total number of data-points :', data.size)
    numerical_features = [f for f in data.columns if data[f].dtypes != 'O']
    print('4) Count of Numerical Features :', len(numerical_features))
    cat_features = [c for c in data.columns if data[c].dtypes == 'O']
    print('5) Count of Categorical Features :', len(cat_features))


def features_with_missing_values(data):
    """
    Missing value identification
    :param data:
    :return:
    """
    x = data.isnull().sum().sum() / (data.shape[0] * data.shape[1]) * 100
    print('Percentage of Total Missing Values is ', round(x, 2), '%')
    print('Missing Value Estimation :')
    for i in data.columns:
        if data[i].isna().sum() > 0:
            print('The Feature ', i, ' has ' + str(data[i].isna().sum()) + ' missing values')


def plot_correlation_matrix(data):
    """
    Plotting correlation matrix to understand significance of each input feature
    :param data:
    :return:
    """
    corrmap = data.corr()
    top = corrmap.index
    plt.figure(figsize=(30, 20))
    g = sns.heatmap(data[top].corr(), annot=True, cmap="RdYlGn")


def extract_category(dataset):
    dataset['Customer Full Name'] = dataset['Customer Fname'].astype(str) + dataset['Customer Lname'].astype(str)

    # dropping unimportant columns
    data = dataset.drop(
        ['Customer Email', 'Product Status', 'Customer Password', 'Customer Street', 'Customer Fname', 'Customer Lname',
         'Latitude', 'Longitude', 'Product Description', 'Product Image', 'Order Zipcode',
         'shipping date (DateOrders)'], axis=1)

    data['Customer Zipcode'] = data['Customer Zipcode'].fillna(0)

    market = data.groupby('Market')  # Grouping by market
    region = data.groupby('Order Region')
    category = data.groupby('Category Name')
    department = data.groupby('Department Name')
    cat_market = dataset.groupby(['Category Name', 'Market'])

    # get count of all Market "ordered" count wrt to category name
    count = cat_market['Market'].count()
    pass


if __name__ == "__main__":

    data = importing_data()
    extract_category(data)
    pass
