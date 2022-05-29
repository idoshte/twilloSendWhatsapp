
# get the livraries
from arcgis.gis import GIS
import pandas as pd
# the code export csv table with all Apps and urls
portal=GIS(username='kamanData',password='kamandata1234')
users_all = portal.users.search('!esri_ & !portaladmin')
list_items = {}
def get_item(user):
    content_item = user.items()
    for item in content_item:
        list_items[item.itemid] = item
    folders = user.folders
    for folder in folders :
        folder_items = user.items(folder=folder['title'])
        for item in folder_items:
            list_items[item.itemid] = item

for i in range(len(users_all)):
    print(f"extract {users_all[i]} data to excel...")
    get_item(users_all[i])

df=pd.DataFrame(list_items)
df=df.transpose()
df.to_csv("allData.csv",index=False,encoding='utf-8')