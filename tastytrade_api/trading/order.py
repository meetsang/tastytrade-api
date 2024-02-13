import requests
import json
import datetime
#from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
import threading
from tastytrade_api.symbology import to_tastytrade_option_symbol
#import pdb

class TastytradeOrder:
    def __init__(self, session_token: str = None, api_url: str = 'https://api.tastytrade.com/accounts'):
        self.api_url = api_url
        self.session_token = session_token
        self.headers = {
            "Authorization": f"{self.session_token}"
        }

        
    
    def reconfirm_order(self, account_number, order_id):
        """
        Makes a POST request to the /accounts/{account_number}/orders/{order_id}/reconfirm API endpoint to reconfirm an order,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to reconfirm.
            order_id (int): The ID of the order to reconfirm.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}/reconfirm"
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error reconfirming order: {response.status_code} - {response.content}")
    
    def dry_run_order(self, account_number, order_id, order_data):
        """
        Runs through preflights for cancel-replace and edit without routing
        
        Makes a POST request to the /accounts/{account_number}/orders/{order_id}/dry-run API endpoint to run preflights for cancel-replace and edit without routing,
        and returns the response as a JSON object. 

        Args:
            account_number (int): The account number for the order to run preflights on.
            order_id (int): The ID of the order to run preflights on.
            order_data (dict): Dictionary containing the order data to use for the preflight.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}/dry-run"
        response = requests.post(url, headers=self.headers, json=order_data)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error running dry run order: {response.status_code} - {response.content}")

    def get_order(self, account_number, order_id):
        """
        Returns a single order based on the id
        
        Makes a GET request to the /accounts/{account_number}/orders/{order_id} API endpoint to get a single order based on its ID,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to retrieve.
            order_id (int): The ID of the order to retrieve.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting order: {response.status_code} - {response.content}")
        
    def cancel_order(self, account_number, order_id):
        """
        Requests order cancellation

        Makes a DELETE request to the /accounts/{account_number}/orders/{order_id} API endpoint to request order cancellation,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to cancel.
            order_id (int): The ID of the order to cancel.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the DELETE request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error cancelling order: {response.status_code} - {response.content}")
        
    def replace_order(self, account_number, order_id, order_data):
        """
        Replaces a live order with a new one. Subsequent fills of the original order will abort the replacement.

        Makes a PUT request to the /accounts/{account_number}/orders/{order_id} API endpoint to replace a live order with a new one,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to replace.
            order_id (int): The ID of the order to replace.
            order_data (dict): Dictionary containing the order data to use for the replacement.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the PUT request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.put(url, headers=self.headers, json=order_data)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error replacing order: {response.status_code} - {response.content}")

    def edit_order(self, account_number, order_id, order_data):
        """
        Edit price and execution properties of a live order by replacement. Subsequent fills of the original order
        
        Makes a PATCH request to the /accounts/{account_number}/orders/{order_id} API endpoint to edit price and execution properties of a live order by replacement,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the order to edit.
            order_id (int): The ID of the order to edit.
            order_data (dict): Dictionary containing the updated order data to use for the replacement.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the PATCH request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/{order_id}"
        response = requests.patch(url, headers=self.headers, json=order_data)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error editing order: {response.status_code} - {response.content}")
        
    def get_live_orders(self, account_number):
        """
        Returns a list of live orders for the resource


        Makes a GET request to the /accounts/{account_number}/orders/live API endpoint to retrieve a list of live orders,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to retrieve the list of live orders.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/live"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting live orders: {response.status_code} - {response.content}")
        
    def get_orders(self, account_number, per_page=10, page_offset=0, start_date=None, end_date=None, underlying_symbol=None, 
                   status=None, futures_symbol=None, underlying_instrument_type=None, sort='Desc', start_at=None, end_at=None,
                   order_type=None):
        """
        Returns a paginated list of the customer's orders (as identified by the provided authentication token)
        based on sort param. If no sort is passed in, it defaults to descending order.
        
        Makes a GET request to the /accounts/{account_number}/orders API endpoint to retrieve a paginated list of the customer's orders
        based on the provided parameters, and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to retrieve the list of orders.
            per_page (int): The number of orders to return per page.
            page_offset (int): The page offset to use when retrieving orders.
            start_date (str): The start date to use for filtering orders.
            end_date (str): The end date to use for filtering orders.
            underlying_symbol (str): The underlying symbol to use for filtering orders.
            status (list): The status values to use for filtering orders.
            futures_symbol (str): The futures symbol to use for filtering orders.
            underlying_instrument_type (str): The underlying instrument type to use for filtering orders.
            sort (str): The order to sort results in. Accepts 'Desc' or 'Asc'. Defaults to 'Desc'.
            start_at (str): The start date and time to use for filtering orders in full date-time.
            end_at (str): The end date and time to use for filtering orders in full date-time.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders"
        params = {
            "per-page": per_page,
            "page-offset": page_offset,
            "start-date": start_date,
            "end-date": end_date,
            "underlying-symbol": underlying_symbol,
            "status[]": status,
            "futures-symbol": futures_symbol,
            "underlying-instrument-type": underlying_instrument_type,
            "sort": sort,
            "start-at": start_at,
            "end-at": end_at,
            "order-type": order_type
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting orders: {response.status_code} - {response.content}")
        
    def create_order(self, account_number, order):
        """
        Accepts a json document containing parameters to create an order for the client.

        Makes a POST request to the /accounts/{account_number}/orders API endpoint to create a new order for the customer,
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for which to create the order.
            order (dict): The order details to be created.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 CREATED.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders"
        headers = {
            "Authorization": f"{self.session_token}",
            "Content-Type": "application/json"
        }
        #print("here")
        response = requests.post(url, headers=headers, json=order)
        #print("here2")
        # SA 10/19/2023: Commented raising an exception.
        # if response.status_code == 201:
        response_data = response.json()
        #print('response: ', json.dumps(response_data,indent = 4))
        return response_data
        # else:
        #     raise Exception(f"Error creating order: {response.status_code} - {response.content}")
        
    def dry_run_new_order(self, account_number, order_data):
        """
        Accepts a json document containing parameters to create an order and then runs the preflights without placing the order.

        Makes a POST request to the /accounts/{account_number}/orders/dry-run API endpoint to validate a new order without placing it, 
        and returns the response as a JSON object.

        Args:
            account_number (int): The account number for the new order.
            order_data (dict): Dictionary containing the order data to use for validation.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the POST request or if the status code is not 201 Created.
        """
        url = f"{self.api_url}/accounts/{account_number}/orders/dry-run"
        response = requests.post(url, headers=self.headers, json=order_data)
        
        if response.status_code == 201:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error running dry run new order: {response.status_code} - {response.content}")

    def get_customer_live_orders(self, customer_id):
        """
        Returns a list of live orders for the customer.

        Makes a GET request to the /customers/{customer_id}/orders/live API endpoint to retrieve a list of live orders for the customer,
        and returns the response as a JSON object.

        Args:
            customer_id (int): The ID of the customer for which to retrieve live orders.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/customers/{customer_id}/orders/live"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            raise Exception(f"Error getting live orders for customer {customer_id}: {response.status_code} - {response.content}")
        
    def get_customer_orders(self, customer_id, per_page=10, page_offset=0, start_date=None, end_date=None,
                             underlying_symbol=None, status=None, futures_symbol=None, underlying_instrument_type=None,
                             sort='Desc', start_at=None, end_at=None):
        """
        Returns a paginated list of the customer's orders based on sort param. 
        If no sort is passed in, it defaults to descending order.
        
        Makes a GET request to the /customers/{customer_id}/orders API endpoint for the authenticated customer's orders,
        and returns a paginated list of the orders.

        Args:
            customer_id (int): The ID of the customer whose orders to retrieve.
            per_page (int): The number of orders to retrieve per page.
            page_offset (int): The page offset to retrieve (e.g. 0 for the first page, 10 for the second, etc.).
            start_date (str): The start date to filter orders by (in yyyy-mm-dd format).
            end_date (str): The end date to filter orders by (in yyyy-mm-dd format).
            underlying_symbol (str): The underlying symbol to filter orders by.
            status (list[str]): A list of order statuses to filter by (e.g. ['Filled', 'Working']).
            futures_symbol (str): The futures symbol to filter orders by.
            underlying_instrument_type (str): The underlying instrument type to filter orders by.
            sort (str): The order to sort results in. Accepts 'Desc' or 'Asc'. Defaults to 'Desc'.
            start_at (str): DateTime start range for filtering orders in full date-time.
            end_at (str): DateTime end range for filtering orders in full date-time.

        Returns:
            list: List of order objects, as returned by the API.

        Raises:
            Exception: If there was an error in the GET request or if the status code is not 200 OK.
        """
        url = f"{self.api_url}/customers/{customer_id}/orders"
        params = {
            "per-page": per_page,
            "page-offset": page_offset,
            "start-date": start_date,
            "end-date": end_date,
            "underlying-symbol": underlying_symbol,
            "status[]": status,
            "futures-symbol": futures_symbol,
            "underlying-instrument-type": underlying_instrument_type,
            "sort": sort,
            "start-at": start_at,
            "end-at": end_at
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            response_data = response.json()
            orders = response_data["data"]["items"]
            return orders
        else:
            raise Exception(f"Error getting customer orders: {response.status_code} - {response.content}")
        
    def getFillPriceMarket(self, account_number, symbol, look_minutes_before=1):

        #Todays date and time
        after_time = datetime.datetime.now() - timedelta(minutes=look_minutes_before)

        #Get orders
        response = self.get_orders(account_number, start_date=after_time,
                                    end_date=after_time,
                                    status='Filled', order_type='Market')
        
        

        # Loop through the items list and filter for order_type=market
        netFill = 0.0
        orderID = ""
        for item in response['data']['items']:
            #Convert received-at to datetime with no timezone:
            rec_at = datetime.datetime.strptime(item['received-at'], '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
            if item['order-type'] == 'Market' and \
            rec_at > after_time \
            and item['legs'][0]["symbol"] ==  symbol:
                for fill in item['legs'][0]['fills']:
                    netFill = float(fill['fill-price']) + netFill
                    orderID = item['id']
                #print(item['order-type'] + ": " + item['received-at'] + ": " + item['legs'][0]["symbol"] + ": " + str(netFill))

        return netFill, orderID

    def build1leg(self, action, symbol, type, strike, exp=datetime.date.today(), quantity=1, instrument_type="Equity Option"):
        #finalSymbol = symbol.ljust(6) + exp.strftime("%y%m%d") + type + self.format_strike(strike)
        finalSymbol = to_tastytrade_option_symbol(symbol, strike, type, exp.strftime("%Y-%m-%d"))
        leg = {
            "action": action,
            "symbol": finalSymbol,
            "quantity": quantity,
            "instrument-type": instrument_type
        }
        return leg
    
    @staticmethod
    def build_json(price, legs, time_in_force="Day", order_type="Limit", price_effect="Credit"):
        if order_type == "Limit":
            json_data = {
                "time-in-force": time_in_force,
                "order-type": order_type,
                "price": price,
                "price-effect": price_effect,
                "legs": legs
            }
        else:
            json_data = {
                "time-in-force": time_in_force,
                "order-type": order_type,
                # "price-effect": price_effect,                 Commented Oct 19 2023 No Price-Effect for Market Orders SANG
                "legs": legs
            }
        return json.dumps(json_data, indent=4)
    
    #Short Call, Short Put, Expiry, Amount
    def build_Any_Trade(self, SC, LC, SP, LP, Exp, Amt, type_tr, Ticker = "SPXW", order_type = "Limit"):
        if type_tr[0] == "C":
            strSell = "Sell to Open"
            strBuy = "Buy to Open"
            price_effect = "Credit"
        else:
            strBuy = "Sell to Open"
            strSell = "Buy to Open"
            price_effect = "Debit"

        leg1 = self.build1leg(strSell, Ticker, "C", SC, Exp)
        leg3 = self.build1leg(strSell, Ticker, "P", SP, Exp)
        leg2 = self.build1leg(strBuy,  Ticker, "C", LC, Exp)
        leg4 = self.build1leg(strBuy,  Ticker, "P", LP, Exp)


        if SC == 0:
            #PCS No Wing:
            if LP == 0: 
                legs = [leg3]
            else:
                legs = [leg3, leg4]
        elif SP == 0:
            #CCS No Wing
            if LC == 0: 
                legs = [leg1]
            else:
                legs = [leg1, leg2]
        elif LC == 0 and LP == 0:
            #IF No Wing
            legs = [leg1, leg3]
        else:
            legs = [leg1, leg2, leg3, leg4]

        # Build JSON
        json_string = self.build_json( Amt, legs, "Day", order_type, price_effect)

        # Convert JSON to dictionary
        return json.loads(json_string)
    
    def send_order_from_leg(self, account_number, Amt, leg, time_in_force, order_type, price_effect):
        # Build JSON
        json_string = self.build_json( Amt, leg, time_in_force, order_type, price_effect)
        # Convert JSON to dictionary
        data_dict = json.loads(json_string)
        #Send order
        return data_dict, self.create_order(account_number, data_dict)
        #order_list = str(order_list) + ";" + str(df_all_legs[index, "response"]['data']['order']['id'])

        
    #Build any trade, place order and negotiate: 
    # Short Call, Short Put, Long Call, Long Put, Expiry, Amount, type of trade, Ticker, Order Type, Sleep Timer, Reduce Price by, Repeat times 
    def build_Any_Trade_AND_place_order(self, account_number, Qty, SC, LC, SP, LP, Exp, Amt, type_tr, Ticker, order_type, slpTimeSec, reducePriceBy, repeat_n_times: int):
        if type_tr[0] == "C":
            strSell = "Sell to Open"
            strBuy = "Buy to Open"
            price_effect = "Credit"
            reverse_price_effect = "Debit"
        else:
            strBuy = "Sell to Open"
            strSell = "Buy to Open"
            price_effect = "Debit"
            reverse_price_effect = "Credit"

        leg1 = self.build1leg(strSell, Ticker, "C", SC, Exp, Qty)
        leg3 = self.build1leg(strSell, Ticker, "P", SP, Exp, Qty)
        leg2 = self.build1leg(strBuy,  Ticker, "C", LC, Exp, Qty)
        leg4 = self.build1leg(strBuy,  Ticker, "P", LP, Exp, Qty)

        if type_tr[0] == "C":
            all_legs = {
                "leg_names": ["LC", "LP", "SC", "SP"],
                "legs": [leg2, leg4, leg1, leg3],
                "strikes": [LC, LP, SC, SP,],
                "price_effect":[reverse_price_effect, reverse_price_effect, price_effect, price_effect],
                "multiply": [1,1,-1,-1]
            }
        else:
            all_legs = {
                "leg_names": ["SC", "SP", "LC", "LP"],
                "legs": [leg1, leg3, leg2, leg4],
                "strikes": [SC, SP, LC, LP],
                "price_effect":[price_effect, price_effect, reverse_price_effect, reverse_price_effect],
                "multiply": [-1,-1,1,1]
            }

        order_list = None
        fillPrice = 0
        #Multi-Legs Limit:
        if order_type == "Limit":
            if SC == 0:
                #PCS No Wing:
                if LP == 0: 
                    legs = [leg3]
                else:
                    legs = [leg3, leg4]
            elif SP == 0:
                #CCS No Wing
                if LC == 0: 
                    legs = [leg1]
                else:
                    legs = [leg1, leg2]
            elif LC == 0 and LP == 0:
                #IF No Wing
                legs = [leg1, leg3]
            else:
                legs = [leg1, leg2, leg3, leg4]

            # Send Order
            data_dict, response = self.send_order_from_leg(account_number, Amt, legs, "Day", order_type, price_effect)
            
            if "error" in response:
                print("Error in placing trade")
                order_list = "error"
                fillPrice = 666
            else:
                order_list = str(response['data']['order']['id'])

                #negotiate order:
                order_list = str(self.negotiate_price2(account_number, response['data']['order']['id'], slpTimeSec, reducePriceBy, data_dict, repeat_n_times))

                #Get Fill Price:
                fillPrice = self.getOrderFillAmt(account_number, int(order_list))
        
        #Market Orders Individual
        else:
            #create dataframe from the all_legs:
            df_all_legs = pd.DataFrame(all_legs)

            # print(df_all_legs)

            #Loop and send indv orders:
            for index, row in df_all_legs.iterrows():
                if row["strikes"] != 0:
                    try:
                        # Send Order
                        df_all_legs[index, "data_dict"], df_all_legs[index, "response"] = \
                            self.send_order_from_leg(account_number, 0, [row["legs"]], "Day", order_type, row["price_effect"])
                        time.sleep(2)
                    except:
                        continue
                    


            #This did not work, instead the below loop will go back and get the filled orders in last minute
            #Loop and get order_list and fills:
            # for index, row in df_all_legs.iterrows():
            #     if row["strikes"] != 0:
            #         try:
            #             order_list = str(order_list) + ";" + str(df_all_legs[index, "response"]['data']['order']['id'])
            #             fillPrice = fillPrice + (row["multiply"] * self.getOrderFillAmt(account_number, df_all_legs[index, "response"]['data']['order']['id']))
            #         except:
            #             continue

            #Get filled market orders numbers and fill prices. Need to wait.
            time.sleep(4) 
            order_list = ""
            for index, row in df_all_legs.iterrows():
                if row["strikes"] != 0:
                    fillPrice1, orderID1 = self.getFillPriceMarket(account_number,row["legs"]["symbol"], 1)
                    print(row["legs"]["symbol"] + ": " + str(fillPrice1)+ ": " + str(orderID1))
                    fillPrice = fillPrice + row["multiply"] * fillPrice1
                    order_list = order_list + ";" + str(orderID1)


        return order_list, fillPrice



    #Short Call, Short Put, Expiry, Amount
    def build_Cr_IF(self, SC, LC, SP, LP, Exp, Amt, Ticker = "SPXW", No_Wings=False):
        # Build legs
        leg1 = self.build1leg("Sell to Open", Ticker, "C", SC, Exp)
        leg3 = self.build1leg("Sell to Open", Ticker, "P", SP, Exp)
        
        # Combine legs
        if No_Wings:
            legs = [leg1, leg3]
        else:    
            leg2 = self.build1leg("Buy to Open",  Ticker, "C", LC, Exp)
            leg4 = self.build1leg("Buy to Open",  Ticker, "P", LP, Exp)
            legs = [leg1, leg2, leg3, leg4]

        # Build JSON
        json_string = self.build_json( Amt, legs)

        # Convert JSON to dictionary
        return json.loads(json_string)
    
    #Short Call, Short Put, Expiry, Amount
    def build_Db_IF(self, SC, LC, SP, LP, Exp, Amt, Ticker = "SPXW",  No_Wings=False):
        # Build legs
        leg1 = self.build1leg("Buy to Open", Ticker, "C", SC, Exp)
        leg3 = self.build1leg("Buy to Open", Ticker, "P", SP, Exp)

        # Combine legs
        if No_Wings:
            legs = [leg1, leg3]
        else: 
            leg2 = self.build1leg("Sell to Open",  Ticker, "C", LC, Exp) 
            leg4 = self.build1leg("Sell to Open",  Ticker, "P", LP, Exp) 
            legs = [leg1, leg2, leg3, leg4]

        # Build JSON
        json_string = self.build_json( Amt, legs, "Day", "Limit", "Debit")

        # Convert JSON to dictionary
        return json.loads(json_string)

    #Short Call, Short Put, Expiry, Amount
    def build_Cr_IF_Shorts(self, SC, SP, Exp, Amt, Ticker = "SPXW"):
        # Build legs
        leg1 = self.build1leg("Sell to Open", Ticker, "C", SC, Exp)

        leg3 = self.build1leg("Sell to Open", Ticker, "P", SP, Exp)



        # Combine legs
        legs = [leg1, leg3]

        # Build JSON
        json_string = self.build_json( Amt, legs)

        # Convert JSON to dictionary
        return json.loads(json_string)
    
    
        
    def negotiate_price(self, account_number, order_number, slpTimeSec, reducePriceBy, data_dict, repeat_n_times: int):        
        for i in range(repeat_n_times):
            time.sleep(slpTimeSec)
            
            if data_dict["price-effect"] == "Credit":
                data_dict["price"] = str(float(data_dict["price"]) - reducePriceBy)
            else:
                data_dict["price"] = str(float(data_dict["price"]) + reducePriceBy)

            response = self.edit_order(account_number, order_number, data_dict)
            data_dict = response["data"]  
            order_number = response['data']['id']
            print(str(order_number) + ":" + str(data_dict["price"]) + ":" + data_dict["status"]) 

    #Negotiate with returning order number
    def negotiate_price2(self, account_number, order_number, slpTimeSec, reducePriceBy, data_dict, repeat_n_times: int):
        for i in range(repeat_n_times):
            time.sleep(slpTimeSec)            
            try:
                lastPrice = data_dict["price"]
                if data_dict["price-effect"] == "Credit":
                    data_dict["price"] = str(float(data_dict["price"]) - reducePriceBy)
                else:
                    data_dict["price"] = str(float(data_dict["price"]) + reducePriceBy)

                response = self.edit_order(account_number, order_number, data_dict)
                data_dict = response["data"]
                order_number = response['data']['id']
                # print(str(order_number) + ":" + str(data_dict["price"]) + ":" + data_dict["status"])
            except Exception as e:
                break
        return order_number
    
    
    

    def getOrderFillAmt(self, account_number, order_number):
        
        #Get order
        response = self.get_order(account_number, order_number)
        netAmt = 0
        #print('response: ', json.dumps(response,indent = 4))
        for leg in response['data']['legs']:
            for fill in leg['fills']:
                if 'Buy' in leg['action']:
                    netAmt = netAmt + (-1) * float(fill['fill-price']) * float(fill['quantity'])
                elif 'Sell' in leg['action']:
                    netAmt = netAmt + float(fill['fill-price']) * float(fill['quantity'])
        
        return round(netAmt/response['data']['size'],2)
