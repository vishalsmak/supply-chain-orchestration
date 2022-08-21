import pandas as pd
import numpy as np

class DataExtractor:
    def __init__(self, filepath):
        self.category_list = None
        self.country_list = None
        self.delivery_risk = None
        self.dropped_data = None

        data = self.importing_data()
        self.calculate_correlation(data)
        self.extract_category(data)
    
    def importing_data(self, filepath):
        data = pd.read_csv(filepath, header=0, encoding='unicode_escape')
        pd.set_option('display.max_columns', None)
        return data

    def get_category_list(self) -> list:
        return self.category_list

    def get_delivery_risk_mean(self):
        return self.delivery_risk

    def get_dropped_data(self):
        return self.dropped_data

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