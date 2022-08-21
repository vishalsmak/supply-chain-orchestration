import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class AppData:

    def __init__(self):
        self.category_list = None
        self.country_list = None
        self.delivery_risk = None
        self.data_headers = None
        self.dropped_data = None

        self.corrmap = None
        data = self.importing_data()
        self.calculate_correlation(data)
        self.extract_category(data)

    def importing_data(self):
        """
        Importing dataset from local directory
        :return:
        """
        data = pd.read_csv('/Users/vishal/Documents/code/supply-chain-orchestration/src/scm-dataset/SupplyChainDataset.csv',
                           header=0, encoding='unicode_escape')
        pd.set_option('display.max_columns', None)
        return data

    def get_category_list(self) -> list:
        return self.category_list

    def get_delivery_risk_mean(self):
        return self.delivery_risk

    def get_correlation(self):
        return self.corrmap

    def get_headers(self):
        return self.data_headers

    def get_dropped_data(self):
        return self.dropped_data

    def extract_shipment_features(self, data):
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


    def extract_financial_features(self, data):
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


    def data_info(self, data):
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


    def features_with_missing_values(self, data):
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


    def plot_correlation_matrix(self, data):
        """
        Plotting correlation matrix to understand significance of each input feature
        :param data:
        :return:
        """
        corrmap = data.corr()
        top = corrmap.index
        plt.figure(figsize=(30, 20))
        g = sns.heatmap(data[top].corr(), annot=True, cmap="RdYlGn")

    def extract_category(self, dataset):
        geo_df = dataset[['Category Name', 'Order Country', 'Order Item Quantity']].copy()
        geo_df_grouped = geo_df.groupby(['Category Name', 'Order Country']).sum()
        geo_df_ind = geo_df_grouped.reset_index()
        self.category_list = list(set(geo_df_ind['Category Name'].tolist()))
        self.country_list = list(set(geo_df_ind['Order Country'].tolist()))

        category_to_index = dict(zip(self.category_list, np.arange(len(self.category_list))))
        country_to_index = dict(zip(self.country_list, np.arange(len(self.country_list))))
        output = np.zeros((len(country_to_index), len(category_to_index)))

        for index, row in geo_df_ind.iterrows():
            cou = row['Order Country']
            cat = row['Category Name']
            qty = row['Order Item Quantity']
            cou_idx = country_to_index[cou]
            cat_idx = category_to_index[cat]
            output[cou_idx, cat_idx] = qty

        final_df = pd.DataFrame(data=output, index=self.country_list, columns=self.category_list)
        delivery_exp = dataset[['Order Country', 'Late_delivery_risk']].copy()
        self.delivery_risk = delivery_exp.groupby(['Order Country']).mean().reset_index()

    def calculate_correlation(self, data):

        data['Customer Full Name'] = data['Customer Fname'].astype(str) + data['Customer Lname'].astype(str)
        data = data.drop(
            ['Customer Email', 'Product Status', 'Customer Password', 'Customer Street', 'Customer Fname', 'Customer Lname',
             'Latitude', 'Longitude', 'Product Description', 'Product Image', 'Order Zipcode',
             'shipping date (DateOrders)', 'Order State'], axis=1)
        data['Customer Zipcode'] = data['Customer Zipcode'].fillna(0)

        self.dropped_data = data
        self.data_headers = list(self.dropped_data)
        self.corrmap = data.corr()

