#importing libraries
from csv import writer
import requests
import json
import pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
#Here, data extraction is done for the category: Snacks and Branded Foods
root_url = requests.get('https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug=snacks-branded-foods',headers=header) 

info = json.loads(root_url.text)
tab = info['tab_info']
lst = []
for i in tab[0]['header_section']['items']:
    lst.append(i)
    
slug = []
for j in lst:
    slug.append(j['slug'])
for x in slug:
    node_url = requests.get('https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug={x}'.format(x=x), headers=header)
    node_info = json.loads(node_url.text)
    node_tab = node_info['tab_info']
    new_lst = []
    
    for i in node_tab[0]['header_section']['items']:
        new_lst.append(i)
    cat = []
    qty = []
    lvl = []
    new_slugs = []
    for j in new_lst:
        lvl.append(j['level'])
        cat.append(j['title']['text'])
        qty.append(j['count'])
        new_slugs.append(j['slug']

    #print values as a data frame
    bigb = {'Level': lvl, 'Category Name':cat, 'Quantity':qty}
    df = pd.DataFrame.from_dict(bigb)
    #print(df)
    df.to_csv('catgories.csv', mode='a', header=True)
    
    #to extract product details                     
    for y in new_slugs:
        base_url = requests.get('https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug={y}'.format(y=y), headers=header)
            base_info = json.loads(base_url.text)
            base_tab = base_info['tab_info']
            base_lst = []
            for i in base_tab[0]['product_info']['products']:
                lst.append(i)

            name = []
            mrp = []
            qty = []
            code = []
            brand = []
            link = []
            for j in lst:
                name.append(j['p_desc'])
                mrp.append(j['mrp'])
                qty.append(j['w'])
                code.append(j['sku'])
                brand.append(j['p_brand'])
                link.append(j['absolute_url'])

        bigb = {'Product Name':name, 'Price':mrp, 'Quantity':qty, 'Code':code, 'Brand':brand, 'Product Link':link}
        df = pd.DataFrame.from_dict(bigb)
        #print(df)
        df.to_csv('bakery.csv', mode='a', header=True)
