import urllib.request as req
import json
import math
import time
import csv

# 初始頁數
page = 1

# 儲存所有商品的 ID
all_prod_ids = []
five_star_prod_ids = []
i5_prod_ids = []
PCs_ids=[]
output_matrix=[]
output_all=[]

while True:
    # PChome URL網址
    url = f"https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAA31&attr=&page={page}"

    # 建立一個 Request 物件，附加 Request Headers 資訊
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })

    # 發送請求並取得回應
    with req.urlopen(request) as response:
        PC_data = response.read().decode("utf-8")  # 回應的資料是 JSON 格式

    # 解析 JSON 格式資料
    PC_data = json.loads(PC_data)

    # 檢查是否有商品資料
    if "Prods" in PC_data and PC_data["Prods"]:
        prod_ID = PC_data["Prods"]  # 確保使用正確的 key
       
        for prodt in prod_ID:                               # Task1&2 code
            all_prod_ids.append(prodt["Id"])
            #print(prodt["Id"])
            if prodt["ratingValue"] == "None" or prodt["ratingValue"] is None:  # 檢查兩種情況
                prodt["ratingValue"] = 0  # 替換為0
                
        for prodtRating in prod_ID:
            if prodtRating["ratingValue"] > 4.9:
              five_star_prod_ids.append(prodtRating["Id"])
              #print(prodtRating["Id"])  # 印出>4.9星商品 ID

        for prodt in prod_ID:                               #Task3 code
            if "i5" in prodt["Name"]:
                i5_prod_ids.append(prodt["Price"])
                #print(prodt["Id"])

        for prodt in prod_ID:
          PCs_ids.append(prodt["Price"])
          first_rows=[prodt["Id"],prodt["Price"]]
          output_matrix.append(first_rows)

        # 進入下一頁
        page += 1

        # 避免請求過快，稍作延遲
        time.sleep(1)
    else:
        # 如果沒有更多商品資料，結束爬取

        break

# 總結結果
average_price = sum(i5_prod_ids) / len(i5_prod_ids)
total_average_price = sum(PCs_ids) / len(PCs_ids)
squared_differences = [(x - total_average_price)**2 for x in PCs_ids]
variance = sum(squared_differences) / len(squared_differences)
std_dev = math.sqrt(variance)
# 正確計算 Z 分數的方法
Zscores = [(x - total_average_price) / std_dev for x in PCs_ids] # 對每個數值計算 Z 分數
# print(Zscores)
# print(output_matrix)
Result=zip(output_matrix, Zscores)
#print(list(Result))
for FL in Result:
    output_matrix, Zscores=FL
    Ids,Prices=output_matrix
    output_all.append([Ids,Prices,Zscores])
#print(output_all)

# # 將product.txt輸出                                       # Task1 code
# filename = "products.txt"  # 設定檔案名稱

# with open(filename, "w") as file:  # 使用 with open() 確保檔案正確關閉
#     for prod_id in all_prod_ids:
#         file.write(str(prod_id) + "\n")  # 將每個 ID 轉換成字串並加上換行符號

# #將best-product.txt輸出                                   # Task2 code
# filename = "best-products.txt"  # 設定檔案名稱

# with open(filename, "w") as file:  # 使用 with open() 確保檔案正確關閉
#     for prod_id in five_star_prod_ids:
#         file.write(str(prod_id) + "\n")  # 將每個 ID 轉換成字串並加上換行符號

# filename = "standardization.csv"
# with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     # 移除或註解掉以下這行，即可不寫入標題列
#     # writer.writerow(["ProductID", "Price", "PriceZScore"])
#     writer.writerows(output_all)



print(f"平均價格為{average_price}")
print(f"共爬取 {len(i5_prod_ids)} 筆i5 processor商品資料")
print(f"共爬取 {len(five_star_prod_ids)} 筆5星商品資料")
print(f"共爬取 {len(all_prod_ids)} 筆商品資料")