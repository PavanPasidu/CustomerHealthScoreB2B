import Constant as const
import GetServicenowData as snd
import csv

class ConverttoCSV:
    def __init__(self,constant,servicenow):
        self.servicenow     =   servicenow
        self.constant       =   constant

    def getData(self):
        caseData    =   self.servicenow.getJSONpayload(const=self.constant,url='https://wso2sndev.service-now.com/api/wso2/customer_health/get_ticket_history')
        accountData =   self.servicenow.getJSONpayload(const=self.constant,url='https://wso2sndev.service-now.com/api/wso2/customer_health/get_product_details')

        # convert data into csv format
        caseDatapath    =   self.convertData(caseData,filename='case_data.csv',special=True)
        accountDatapath =   self.convertData(accountData,filename='account_data.csv',special=False)

        return caseDatapath,accountDatapath
    

    def convertData(self,dataJson,filename,special):
        # Extract header fields from the first JSON object
        dataField       = dataJson['result']['data']

        if special:
            acc_name        = list(dataField[0].keys())
            header_fields   = list(dataJson["result"]["data"][0][acc_name[0]].keys()) + ["account_name"]
        else:
            header_fields   = dataField[0].keys()

        # Specify the name of the CSV file
        csv_filepath = f"E:/Research/CHS_Repo/CustomerHealthScoreB2B/Data/{filename}"

        # Write JSON data to CSV file
        with open(csv_filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header_fields)
            
            # Write header
            writer.writeheader()
            
            # Write data
            if special:
                for item in dataField:
                    account_name, data = next(iter(item.items()))
                    data["account_name"] = account_name  
                    writer.writerow(data)
            else:
                for item in dataField:
                    writer.writerow(item)

        return csv_filepath