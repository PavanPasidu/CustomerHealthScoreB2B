from ..Constant import Constant as const
from ..Servicenow.GetServicenowData import GetServicenowData as snd
import csv
import pandas as pd

class ConverttoCSV:
    def __init__(self,constant,servicenow):
        self.servicenow     =   servicenow
        self.constant       =   constant

    def getData(self):
        caseData    =   self.servicenow.getJSONpayload(const=self.constant,url='https://wso2sndev.service-now.com/api/wso2/customer_health/get_ticket_history')
        accountData =   self.servicenow.getJSONpayload(const=self.constant,url='https://wso2sndev.service-now.com/api/wso2/customer_health/get_product_details')

        # convert data into csv format
        caseDatapath    =   self.convertData(caseData,special=True)
        accountDatapath =   self.convertData(accountData,special=False)

        return caseDatapath,accountDatapath
    

    
    def convertData(self, dataJson, special):
        # Extract header fields from the first JSON object
        dataField = dataJson['result']['data']

        if special:
            acc_name = list(dataField[0].keys())
            header_fields = list(dataJson["result"]["data"][0][acc_name[0]].keys()) + ["account_name"]
        else:
            header_fields = dataField[0].keys()

        # Prepare data for DataFrame
        if special:
            rows = []
            for item in dataField:
                account_name, data = next(iter(item.items()))
                data["account_name"] = account_name
                rows.append(data)
        else:
            rows = dataField

        # Create DataFrame
        df = pd.DataFrame(rows, columns=header_fields)
        return df