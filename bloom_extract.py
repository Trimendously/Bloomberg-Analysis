import logging
import os,sys


import blpapi
import pandas as pd
import json


# Loads the cached data if we don't have access to a bloomberg terminal
def cached_bloom_data():
    try:
        with open("cached_data/spx_members.json", "r") as file:
            data = json.load(file)
            # Need to add date in json
            error_message = "Connection Error\nUsing cached Bloomberg Terminal data"
                     
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(f"Error loading the cached Bloom data: {err}")
        error_message = "Connection Error\nNo cached data exists"
        data = []

    df_bloom = pd.DataFrame(data)
    return df_bloom,error_message



def bloom_data():

    def company_reference_data(member_ticker):
        company_request = refDataService.createRequest("ReferenceDataRequest")
        company_request.append("securities", member_ticker + " EQUITY")
        company_request.append("fields", "NAME")
        company_request.append("fields", "INDUSTRY_SECTOR")
        # Temp fix
        company_request.append("fields", "PX_LAST")

        
        # Send the request for company details and wait for the response
        session.sendRequest(company_request)
        while True:
            event = session.nextEvent()
            if event.eventType() == blpapi.Event.RESPONSE:
                break

        # ExtractS the company details from the response
        for msg in event:
            company_dataArray = msg.getElement("securityData")

            for company_data in company_dataArray.values():
                company_name = company_data.getElement("fieldData").getElement("NAME").getValue()
                company_sector = company_data.getElement("fieldData").getElement("INDUSTRY_SECTOR").getValue()
                #Temp
                company_price = company_data.getElement("fieldData").getElement("PX_LAST").getValue()
                return company_name,company_sector,company_price

    #WIP
    def company_historical_data(member_ticker,date):
        company_price_request = refDataService.createRequest("HistoricalDataRequest")
        company_price_request.append("securities", member_ticker + " EQUITY") # The proper ticker ends in equity
        company_price_request.append("fields", "PX_LAST")
        company_price_request.set("startDate", "20220423")
        company_price_request.set("endDate", "20220423")


        # Send the request and waits
        session.sendRequest(company_price_request)
        while True:
            event = session.nextEvent()
            if event.eventType() == blpapi.Event.RESPONSE:
                break
        
        for msg in event:
            print(msg)
            company_dataArray = msg.getElement("securityData")
            for company_data in company_dataArray.values():
                price = company_data.getElement("fieldData").getElement("PX_LAST").getValue()
                #date = company_data.getElement("fieldData").getElement("date").getValue()
                print(price)
                
                return price
        return 1

                
        
    df = pd.DataFrame(columns=['ticker','name','sector'])
    date = "Price (20230423)" # Temporary
    error_message = ""
    try :

        # Start a Bloomberg session
        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost('localhost')
        sessionOptions.setServerPort(8194)
        session = blpapi.Session(sessionOptions)
    
        if not session.start():
            raise Exception("Failed to start session.")

        # Opens a service to get reference data from Bloomberg
        if not session.openService("//blp/refdata"):
            raise Exception("Failed to open //blp/refdata")

        refDataService = session.getService("//blp/refdata")

        # Prepares a request for security data
        request = refDataServifvsdfvdce.createRequest("ReferenceDataRequest")
        request.append("securities", "SPX Index") # S&P 500
        request.append("fields", "INDX_MEMBERS") # Adds the members tickers


        # Sends the request and waits for the response
        session.sendRequest(request)
        while True:
            event = session.nextEvent()
            if event.eventType() == blpapi.Event.RESPONSE:
                break


        # Extract the security data from the response
        company_counter = 0
        for msg in event:
            securityDataArray = msg.getElement("securityData")
            for securityData in securityDataArray.values():
                ticker = securityData.getElement("security").getValue()
                fieldData = securityData.getElement("fieldData")
                memberArray = fieldData.getElement("INDX_MEMBERS")
        

                # For each company
                for member in memberArray:
                    member_ticker = member.getElement("Member Ticker and Exchange Code").getValue().split(' ')[0] # To ignore the exchange code

                    print("Company ",company_counter, " processed.")
                    name,sector,price = company_reference_data(member_ticker)
                    
                    #price = company_historical_data(member_ticker)  

                    member_tickers.append({
                    'ticker': member_ticker,
                    'name': name,
                    'sector': sector,
                    date: price
                    })
                    
                    company_counter += 1

                members_df = pd.DataFrame(member_tickers)
                df = pd.concat([df, members_df], axis=0)

        # Stops the Bloomberg session
        session.stop()

        # Saves the dataframe as a JSON file
        if not os.path.exists("cached_data"):
            os.makedirs("cached_data")
        
        df.to_json("cached_data/spx_members.json", orient='records')
    
    except Exception as e:
        #print("Error accessing the Bloomberg API: ", e,"\nUsing presaved json instead")
        df,error_message = cached_bloom_data()

    finally :
        return df,error_message
