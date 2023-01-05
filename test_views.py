#!/bin/python

import unittest
import requests

url = 'http://172.104.146.107'

class TestViews(unittest.TestCase):

    def test_getMain(self):
        """First test, I try to access the app on the root address"""
        self.assertEqual(requests.get(url).status_code, 200)
    
    def test_getWallet(self):
        """Second test, I try to retrieve my wallet data"""
        self.assertEqual(requests.get(f'{url}/api/wallet').status_code, 200)

    def test_updateWallet_valid_buy(self):
        """Third test, I try to update my wallet by adding new tokens using a valid request"""
        data = {"token" : "BTC", "quantity" : 1, "buying_value" : 15000}
        self.assertEqual(requests.put(f'{url}/api/wallet',json=data).status_code, 200)

    def test_updateWallet_invalid(self):
        """Fourth test, I try to update my wallet by adding new tokens using a invalid request"""
        """(note that all form validation are done on the frontend of the app hence the 500 status code)"""
        data = {"token" : 1, "quantity" : 'aaaa', "buying_value" : True}
        self.assertEqual(requests.put(f'{url}/api/wallet',json=data).status_code, 500)

    def test_history_backup(self):
        """Fifth test, I try to backup the data of my new wallet (1 BTC)"""
        self.assertEqual(requests.get(f'{url}/api/history/backup').status_code, 200)

    def test_request_a_report(self):
        """Sixth test, I try to request a report then get a plot id using a valid request"""
        data = {"token" : "total", "report" : "profit", "period" : "all"}
        self.assertEqual(requests.post(f'{url}/api/history/get',json=data).status_code, 200)

    def test_request_a_report(self):
        """Seventh test, I try to request a report then get a plot id unsing an invalid request"""
        data = {"token" : "Jesuscoin", "report" : "profit", "period" : "all"}
        self.assertEqual(requests.post(f'{url}/api/history/get',json=data).status_code, 500)

    def test_get_graph(self):
        """Eighth test, I try to ask for a report, get a plot ID and access the plot"""
        data = {"token" : "total", "report" : "profit", "period" : "all"}
        response = requests.post(f'{url}/api/history/get',json=data)
        graph_id = response.text
        self.assertEqual(requests.get(f'{url}/api/history/plot/{graph_id}').status_code, 200)
    
if __name__ == "__main__" :
    unittest.main()