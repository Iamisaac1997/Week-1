import urllib.request as req
import json
import math
import time
import csv


page = 1                                                                                            # 起始爬蟲頁數


all_prod_ids = []                                                                                   # 賦值代數
five_star_prod_ids = []
i5_prod_ids = []
PCs_ids=[]
output_matrix=[]
output_all=[]

while True:
    
    url = f"https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAA31&attr=&page={page}"  # PChome URL網址

    
    request = req.Request(url, headers={                                                            # 建立一個 Request 物件，附加 Request Headers資訊
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })                                                                                              

    
    with req.urlopen(request) as response:                                                          # 發送請求並取得回應
        PC_data = response.read().decode("utf-8")                                                   # 回應的資料是 JSON 格式

    PC_data = json.loads(PC_data)                                                                   # 解析 JSON 格式資料

    
    if "Prods" in PC_data and PC_data["Prods"]:                                                     # 檢查是否有商品資料
        prod_ID = PC_data["Prods"]                                                                  # 將網頁data中的Prods賦值到prod_ID
       
        for prodt in prod_ID:                                                                       # 找出所有產品的ID  
            all_prod_ids.append(prodt["Id"])                                                        # all products會放在all_prod_ids (Task1)
            #print(prodt["Id"])
            if prodt["ratingValue"] == "None" or prodt["ratingValue"] is None:                      # 找出所有產品後直接將評論數為None的string換成0
                prodt["ratingValue"] = 0
                
        for prodtRating in prod_ID:
            if prodtRating["ratingValue"] > 4.9:                                                    # 篩選出>4.9星產品
              five_star_prod_ids.append(prodtRating["Id"])                                          # >4.9星products會放在five_star_prod_ids (Task2)
              #print(prodtRating["Id"])                                                             

        for i5_prodt in prod_ID:                                                                       
            if "i5" in i5_prodt["Name"]:                                                            #篩選出i5_prodt內的i5 proessor
                i5_prod_ids.append(i5_prodt["Price"])                                               #篩選出的i5產品會放在i5_prod_ids
                #print(i5_prodt["Id"])

        for Zscore_prodt in prod_ID:
          PCs_ids.append(Zscore_prodt["Price"])                                                     #找出IDs & Prices
          first_rows=[Zscore_prodt["Id"],Zscore_prodt["Price"]]
          output_matrix.append(first_rows)                                                          #IDs&Prices放在output_matrix

        page += 1

        time.sleep(1)                             
    else:

        break


average_price = sum(i5_prod_ids) / len(i5_prod_ids)                                                 #計算i5產品平均價格

total_average_price = sum(PCs_ids) / len(PCs_ids)                                                   #計算Zsocre
squared_differences = [(x - total_average_price)**2 for x in PCs_ids]
variance = sum(squared_differences) / len(squared_differences)
std_dev = math.sqrt(variance)
Zscores = [(x - total_average_price) / std_dev for x in PCs_ids]                                    #對每個數值計算Z-score
# print(Zscores)
# print(output_matrix)

Result=zip(output_matrix, Zscores)                                                                  #把output_matrix與Zscores組合
#print(list(Result))

for FL in Result:                                                                                   #把output_matrix的list拆成IDs和Prices
    output_matrix, Zscores=FL
    Ids,Prices=output_matrix
    output_all.append([Ids,Prices,Zscores])                                                         #重新組合
#print(type(output_all))


filename = "products.txt"                                                                           #輸出product.txt
with open(filename, "w") as file:
    for all_products in all_prod_ids:
        file.write(str(all_products) + "\n")
                                                                                
filename = "best-products.txt"                                                                      #輸出best-product.txt
with open(filename, "w") as file:
    for five_star_products in five_star_prod_ids:
        file.write(str(five_star_products) + "\n")

filename = "standardization.csv"                                                                    #輸出standardization.csv
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_all)



print(f"i5 Processor average price is {average_price}")
# print(f"共爬取 {len(i5_prod_ids)} 筆i5 processor商品資料")
# print(f"共爬取 {len(five_star_prod_ids)} 筆5星商品資料")
# print(f"共爬取 {len(all_prod_ids)} 筆商品資料")