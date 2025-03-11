import unittest
import pandas as pd
import numpy as np
import logging
import os

# Assuming your functions are in a file named 'your_module.py'
# Replace 'your_module' with the actual name of your file.
from your_module import load_data, merge_data  # type: ignore

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Create dummy data for testing
        self.train_data = pd.DataFrame({
            'Store': [1, 2, 3],
            'Sales': [100, 200, 300],
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03']
        })
        self.test_data = pd.DataFrame({
            'Store': [1, 2, 4],
            'Date': ['2023-01-04', '2023-01-05', '2023-01-06']
        })
        self.store_data = pd.DataFrame({
            'Store': [1, 2, 3, 4],
            'StoreType': ['a', 'b', 'c', 'd'],
            'Assortment': ['basic', 'extended', 'basic', 'extended']
        })

        # Create temporary CSV files
        self.train_path = 'train_temp.csv'
        self.test_path = 'test_temp.csv'
        self.store_path = 'store_temp.csv'

        self.train_data.to_csv(self.train_path, index=False)
        self.test_data.to_csv(self.test_path, index=False)
        self.store_data.to_csv(self.store_path, index=False)

        # Setup logging to a test log file.
        logging.basicConfig(level=logging.INFO, filename='test_eda.log',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def tearDown(self):
        # Remove temporary CSV files
        os.remove(self.train_path)
        os.remove(self.test_path)
        os.remove(self.store_path)
        # Remove the test log file.
        if os.path.exists('test_eda.log'):
            os.remove('test_eda.log')

    def test_load_data(self):
        train, test, store = load_data(self.train_path, self.test_path, self.store_path)
        self.assertTrue(isinstance(train, pd.DataFrame))
        self.assertTrue(isinstance(test, pd.DataFrame))
        self.assertTrue(isinstance(store, pd.DataFrame))
        self.assertEqual(train.shape, (3, 3))
        self.assertEqual(test.shape, (3, 2))
        self.assertEqual(store.shape, (4, 3))

    def test_merge_data(self):
        train, test, store = load_data(self.train_path, self.test_path, self.store_path)
        train_merged, test_merged = merge_data(train, test, store)

        self.assertTrue(isinstance(train_merged, pd.DataFrame))
        self.assertTrue(isinstance(test_merged, pd.DataFrame))
        self.assertEqual(train_merged.shape, (3, 5))  # Added StoreType and Assortment
        self.assertEqual(test_merged.shape, (3, 4))   # Added StoreType and Assortment

        # Check if merge was done correctly for store 4.
        self.assertTrue('StoreType' in test_merged.columns)
        self.assertTrue('Assortment' in test_merged.columns)
        self.assertEqual(test_merged.loc[test_merged['Store'] == 4, 'StoreType'].iloc[0], 'd')
        self.assertEqual(test_merged.loc[test_merged['Store'] == 4, 'Assortment'].iloc[0], 'extended')
        self.assertEqual(train_merged.loc[train_merged['Store'] == 1, 'StoreType'].iloc[0], 'a')

if __name__ == '__main__':
    unittest.main()