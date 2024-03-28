
from celery  import shared_task
import logging
import requests
import datetime
from .models import Warehouse,IcgSaleTransactions
import hashlib
from django.db.models import Q
from django.db.utils import IntegrityError
from decimal import Decimal

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def my_task():

    '''get the store details for chicken republic'''
    #url = "https://yanotweb.azurewebsites.net/token"
    url ="http://20.56.133.194/api/v1/store?store_type=CR"
    response = requests.get(url)
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # Convert response to JSON format
        chicken_republic_warehouse_list =[]
        for store_record in data['data']:
            chicken_republic_warehouse_list.append({"warehousename":store_record['store_name'],"warehousecode":store_record['icg_warehouse_code'], "warehousetype":"CR"})
        existing_codes = set(Warehouse.objects.values_list('warehousecode', flat=True))
        # Filter out existing records from the data
        new_records = [record for record in chicken_republic_warehouse_list if record['warehousecode'] not in existing_codes]
        # Bulk insert only the new records
        Warehouse.objects.bulk_create([Warehouse(**record) for record in new_records])
        logger.info('Request to pull the store detail record completed: %s','CR')
    else:
        # Request failed
        logger.info('Request failed to pull the store detail record: %s',response.status_code)
        #print("Request failed to pull the store detail record", response.status_code)

    
    '''get the store details for chicken pie'''
    #url = "https://yanotweb.azurewebsites.net/token"
    url ="http://20.56.133.194/api/v1/store?store_type=PE"
    response = requests.get(url)
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # Convert response to JSON format
        chicken_pie_warehouse_list =[]
        for store_record in data['data']:
            chicken_pie_warehouse_list.append({"warehousename":store_record['store_name'],"warehousecode":store_record['icg_warehouse_code'], "warehousetype":"PE"})
        existing_codes = set(Warehouse.objects.values_list('warehousecode', flat=True))
        # Filter out existing records from the data
        new_records = [record for record in chicken_pie_warehouse_list if record['warehousecode'] not in existing_codes]
        # Bulk insert only the new records
        Warehouse.objects.bulk_create([Warehouse(**record) for record in new_records])
        logger.info('Request to pull the store detail record completed: %s','PE')
    else:
        # Request failed
        logger.info('Request failed to pull the store detail record: %s',response.status_code)
        #print("Request failed to pull the store detail record", response.status_code)

    '''get the store details for chop box'''
    
    #url = "https://yanotweb.azurewebsites.net/token"
    '''
    url ="http://20.56.133.194/api/v1/store?store_type=CB"
    response = requests.get(url)
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # Convert response to JSON format
        chop_box_warehouse_list =[]
        for store_record in data['data']:
            chop_box_warehouse_list.append({"warehousename":store_record['store_name'],"warehousecode":store_record['icg_warehouse_code'], "warehousetype":"CB"})
        existing_codes = set(Warehouse.objects.values_list('warehousecode', flat=True))
        # Filter out existing records from the data
        new_records = [record for record in chop_box_warehouse_list if record['warehousecode'] not in existing_codes]
        # Bulk insert only the new records
        Warehouse.objects.bulk_create([Warehouse(**record) for record in new_records])
        logger.info('Request to pull the store detail record completed: %s','CB')
    else:
        # Request failed
        logger.info('Request failed to pull the store detail record: %s',response.status_code)
        #print("Request failed to pull the store detail record", response.status_code)
    '''

    '''Get the token to access data from ICG '''

    logger.info('Request to get the access token')

    token=''
    url = "https://yanotweb.azurewebsites.net/token"
    response = requests.get(url)
    # Define the data you want to send in the request body
    form_data = {
    'grant_type':'password',
    'username': 'test@fc.com',
    'password': 'Admin@2023_'
    }
    # Send the POST request
    logger.info('Request to get the access token: %s')
   # Define the headers with the content type
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, data=form_data, headers=headers)

    if response.status_code == 200:
        # Print the response content
        data=response.json()
        token = data['access_token']
    else:
        logger.info('Request to get the access token failed with : %s',response.json())
    logger.debug('Data analysis result: %s')

    
    ''' put the record for the previous date'''
  
    # Get today's date
    today = datetime.date.today()

    # Calculate the previous date
    previous_date = today - datetime.timedelta(days=1)

    previous_previous_date = today - datetime.timedelta(days=2)
    # Format the previous date as a string in the required format (YYYY-MM-DD)
    previous_date_str = previous_date.strftime("%Y-%m-%d")

    # Construct the API URL with the previous date as a parameter
    url = f"https://yanotweb.azurewebsites.net/api/FoodConcept/Sales/{previous_date_str}"

    print(url)
    # Define the bearer token
    bearer_token = token

    # Construct the request headers with the bearer token
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    # Make the API request with the headers
    response = requests.get(url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        transaction_entry_list =[]
        try:
            for trans_record in data:
                concatenated_str = f"{trans_record['warehouseCode']}-{trans_record['date']}-{trans_record['paymentType']}"
                unique_value = hashlib.sha256(concatenated_str.encode()).hexdigest()
                transaction_entry_list.append({"warehousecode":trans_record['warehouseCode'],"paymenttype":trans_record['paymentType'], "transactiondate":trans_record['date'],"icgtransactionscode":unique_value,"amount":float(trans_record['amount'])})
            
            existing_transaction_codes = set(IcgSaleTransactions.objects.values_list('icgtransactionscode', flat=True))
            # Create a dictionary to store existing transactions
            existing_transactions_dict = {record.icgtransactionscode: record for record in IcgSaleTransactions.objects.filter(transactiondate__gte=previous_previous_date).filter(transactiondate__lte=previous_date)}
            new_records = []
            existing_records = []
            # Iterate over each record in transaction_entry_list
            for record in transaction_entry_list:
                transaction_code = record['icgtransactionscode']
                if transaction_code in existing_transaction_codes:
                    existing_records.append(record)
                else:
                    new_records.append(record)
            # Bulk create new records
            # Update existing records
            for record in existing_records:
                transaction_code = record['icgtransactionscode']
                amount = Decimal(record['amount'])  # Convert amount to Decimal
                existing_transaction = existing_transactions_dict.get(transaction_code)
                print('existing_transaction')
                print(existing_transaction)
                if existing_transaction:
                    existing_transaction_instance = existing_transaction  # Retrieve the instance
                    existing_transaction_instance.amount = amount  # Assign the new amount
                    existing_transaction_instance.save()
            print(new_records)
            IcgSaleTransactions.objects.bulk_create([IcgSaleTransactions(**record) for record in new_records])
        except IntegrityError as e:
                # Handle the IntegrityError here
                print("IntegrityError occurred:", e)
                pass
                # Example: Print the response data
        logger.info('Completed the storing the transaction data : %s')
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    
    ''' fetch daily transaction for the various stores for the day'''

    