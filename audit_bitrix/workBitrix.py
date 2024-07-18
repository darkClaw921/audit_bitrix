from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
import asyncio
# from workFlask import send_log
import requests
from dealJson import dealJson, fieldsDealJson
load_dotenv()
webhook = os.getenv('WEBHOOK')
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')

bit = Bitrix(webhook)

def send_log(message, level='INFO'):
    requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})






# async def te
def get_deal(dealID:str):
    deal = bit.call('crm.deal.get', items={'id': dealID}, raw=True)['result']
    return deal

def get_lead(leadID:str):
    lead = bit.call('crm.lead.get', params={'id': leadID})
    return lead

def get_deal_fields():
    fields = bit.call('crm.deal.fields',raw=True)['result']
    return fields

def get_all_deals():
    # deals = bit.call('crm.deal.list', raw=True)['result']
    deals=bit.get_all('crm.deal.list',params={'select':['*','UF_*',]})
    return deals




def get_products(poductID):
    products=bit.call('crm.product.get', items={'ID':poductID}, raw=True)['result']
    # products=bit.call('crm.product.get', items={'ID':poductID}, )

    pprint(products)

    return products

def get_users():
    prepareUser = []

    users = bit.call('user.get', raw=True)['result']

    return users

def get_departments():
    departments = bit.call('department.get', raw=True)['result']
    pprint(departments)
    return departments


def get_item(entityID,itemID):
    item=bit.call('crm.item.get', items={'entityTypeId':entityID, 'id': itemID}, raw=True)['result']['item']
    return item


def check_is_full_pole(valuePole:str)->bool:
    if valuePole is None: return False
    valuePole=str(valuePole).strip().lower()
    print(f'{valuePole=}')
    if valuePole in ['','0','0.00','none','[]','{}',[],{},'не выбрано',]:
        return False
    else:
        return True


def get_title_pole(fieldsDeal:dict,key:str)->str:
    # pprint(fieldsDeal)
    fieldValue=fieldsDeal[key].get('formLabel')

    if fieldValue is None:
        poleTitle=fieldsDeal[key]['title']
    else:
        poleTitle=fieldsDeal[key]['formLabel']
    return poleTitle

def check_deal(deal:dict, fieldsDeal:dict):
    # a={}
    global globalFieldsDealJson
    for key, value in deal.items():
        # print(f'{key=}')
        # print(f'{value=}')
        poleTitle=get_title_pole(globalFieldsDealJson,key)
        
        if check_is_full_pole(value):
            fieldsDeal[poleTitle]+=1
        
    # pprint(fieldsDeal)
    return fieldsDeal

def prepare_all_fields_for_deal(fieldsDeal:dict):
    a={}
    for key, value in fieldsDeal.items():
        # print(f'{key=}')
        # print(f'{value=}')
        
        poleTitle=get_title_pole(fieldsDeal,key)

        a[poleTitle]=0     
    return a




def prepare_all_fields_for_contact(fieldsContact:dict):
    a={}
    for key, value in fieldsContact.items():
        # print(f'{key=}')
        # print(f'{value=}')
        
        poleTitle=get_title_pole(fieldsContact,key)

        a[poleTitle]=0     
    return a

def check_contact(contact:dict, fieldsContact:dict):
    # a={}
    global globalFieldsContactJson
    for key, value in contact.items():
        # print(f'{key=}')
        # print(f'{value=}')
        poleTitle=get_title_pole(globalFieldsContactJson,key)
        
        if check_is_full_pole(value):
            fieldsContact[poleTitle]+=1
        
    # pprint(fieldsDeal)
    return fieldsContact

def get_contact_fields():
    fields = bit.call('crm.contact.fields',raw=True)['result']
    return fields

def get_all_contacts():
    # deals = bit.call('crm.deal.list', raw=True)['result']
    contacts=bit.get_all('crm.contact.list',params={'select':['*','UF_*',]})
    return contacts




def get_all_companies():
    companies=bit.get_all('crm.company.list',params={'select':['*','UF_*']})
    pprint(companies)
    1/0
    return companies

def check_company(company:dict, fieldsCompany:dict):
    # a={}
    global globalFieldsCompanyJson
    for key, value in company.items():
        # print(f'{key=}')
        # print(f'{value=}')
        poleTitle=get_title_pole(globalFieldsCompanyJson,key)
        
        if check_is_full_pole(value):
            fieldsCompany[poleTitle]+=1
        
    # pprint(fieldsDeal)
    return fieldsCompany

def prepare_all_fields_for_company(fieldsCompany:dict):
    a={}
    for key, value in fieldsCompany.items():
        # print(f'{key=}')
        # print(f'{value=}')
        
        poleTitle=get_title_pole(fieldsCompany,key)

        a[poleTitle]=0     
    return a

def get_company_fields():
    fields = bit.call('crm.company.fields',raw=True)['result']
    # pprint(fields)
    # 1/0
    return fields

def main():
    global globalFieldsDealJson, globalFieldsContactJson,globalFieldsCompanyJson 
    
    СДЕЛКИ
    fieldsDealJson=get_deal_fields()
    globalFieldsDealJson=fieldsDealJson
    allFields=prepare_all_fields_for_deal(fieldsDealJson)
    
    deals=get_all_deals()
    for deal in deals:
        check_deal(deal, allFields)
    
    pprint(allFields)
    print(f"{'deal':=^50}")
    for key, value in allFields.items():
        print(f'{key} - {value} / {len(deals)} => {value/len(deals)*100:.1f}%')
    
    
    КОНТАКТЫ
    fieldsContact=get_contact_fields()
    globalFieldsContactJson=fieldsContact
    allFields=prepare_all_fields_for_contact(fieldsContact)
    сontacts=get_all_contacts()
    for contact in сontacts:
        check_contact(contact, allFields)
    
    pprint(allFields)
    print(f"{'contact':=^50}")
    for key, value in allFields.items():
    #     print(f'{key} - {value} / {len(сontacts)} => {value/len(сontacts)*100:.1f}%')



    # КОМПАНИИ
    fieldsCompany=get_company_fields()
    globalFieldsCompanyJson=fieldsCompany
    allFields=prepare_all_fields_for_company(fieldsCompany)
    companies=get_all_companies()
    for company in companies:
        check_company(company, allFields)

    pprint(allFields)
    print(f"{'company':=^50}")
    for key, value in allFields.items():
        print(f'{key} - {value} / {len(companies)} => {value/len(companies)*100:.1f}%')



    # pprint(fieldsDeal)
    
    # print(f'{len(deals)=}') 
    # pprint(deals[0])  
    
main()
# a=get_contact_fields()
# pprint(a)
    