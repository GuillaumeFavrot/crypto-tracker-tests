#!/bin/python

import unittest
import requests

url = 'http://172.104.146.107'

class TestViews(unittest.TestCase):

    # First test, I try to access the app on the root address
    def test_getMain(self):
        self.assertEqual(requests.get(url).status_code, 200)
    
    # Second test, I try to retrieve my wallet data 
    def test_getWallet(self):
        self.assertEqual(requests.get(f'{url}/api/wallet').status_code, 200)

    # Third test, I try to update my wallet by adding new tokens using a valid request
    def test_updateWallet_valid_buy(self):
        data = {"token" : "BTC", "quantity" : 1, "buying_value" : 15000}
        self.assertEqual(requests.put(f'{url}/api/wallet',json=data).status_code, 200)

    # Fourth test, I try to update my wallet by adding new tokens using a invalid request 
    # (note that all form validation are done on the frontend of the app hence the 500 status code)
    def test_updateWallet_invalid(self):
        data = {"token" : 1, "quantity" : 'aaaa', "buying_value" : True}
        self.assertEqual(requests.put(f'{url}/api/wallet',json=data).status_code, 500)

    # Fifth test, I try to backup the data of my new wallet (1 BTC)
    def test_history_backup(self):
        self.assertEqual(requests.get(f'{url}/api/history/backup').status_code, 200)

    # Sixth test, I try to request a report then get a plot id and finally retrive a plot with the id 
    def test_request_a_report(self):
        data = {"token" : "total", "report" : "profit", "period" : "all"}
        self.assertEqual(requests.post(f'{url}/api/history/get',json=data).status_code, 200)
    
    # seventh test, I try to get access to my history data    
    def test_get_graph(self):
        data = {"token" : "total", "report" : "profit", "period" : "all"}
        response = requests.post(f'{url}/api/history/get',json=data)
        graph_id = response.text
        self.assertEqual(requests.get(f'{url}/api/history/plot/{graph_id}').status_code, 200)
    
if __name__ == "__main__" :
    unittest.main()