from arcgis.gis import GIS
import pandas as pd

portal=GIS(username='kamanData',password='kamandata1234')

#set "max_users" parameters in search() if you have more than 100 users in your portal
users_all = portal.users.search() 

def get_item(user):
    list_items = {}
    content_item = user.items()
    for item in content_item:
        list_items[item.itemid] = item
        folders = user.folders
    for folder in folders :
        folder_items = user.items(folder=folder['title'])
    for item in folder_items:
        list_items[item.itemid] = item
    df=pd.DataFrame(list_items).transpose().to_excel(str(user.username)+'.xlsx')
for i in range(len(users_all)):
    print("extract "+ str(users_all[i]) + "data to excel...")
    get_item(users_all[i])