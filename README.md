# 專案說明
此專案為「公開資訊觀測站」網路爬蟲, 可下載公司財報, 解析XBRL格式.

# 使用說明
* 從公開資訊觀測站下載財報
  * python3 parser.py -t download_category_xml -c config.json
  * -c：可以指定config name. config file, 需要放在porject_config下
  * 會根據config['kind_list']裡的種類依序下載zip
  * zip會儲存在config['zip_folder'] 
*  把zip解開, 放到config[kind]['xml_folder']
*  產生公司股票代號與全名(目前專案下面已經有處理好的stock_map file. 這個步驟可以省略)
    * 把財報filename裡的股票代號找出來, 產生stock_list.json (只有股票代號）
      * python3 parser.py -t parse_stock_list -c config.json
      * stock_list json會儲存在config[kind]['board_fodler']下
    * 根據股票代號清單, 下載board html
      * python3 parser.py -t download_board -c config.json
      * board xml會儲存在config[kind]['board_folder']
    * 從董監事html, 找出公司全名
      * python3 parser.py -t parse_stock_name -c config.json
      * stock_map.json會儲存在config[kind]['stock_map_json']
      * Possible Error case:
        * parse_stock_name fail=
  * parse財報, 產生json output
    * python3 parser.py -t parse_folder -c config.json
    * json files會儲存在config[kind]['mops_folder']
    * 每個股票代號下面會有三個檔案: 
      * {stock}_{year}.json, {stock}_{year}_name.json, {stock}_{year}_china.json
      * Possible Error case:
        * We can't find some stock in stock_map, missing stock=
  * 處理董監事資料: 
    * python3 parser.py -t parse_board_folder -c config.json
    * board.csv會產生在config[kind]['board_folder']
    * 檢查董監事資料是否完整: 比較board.csv裡面的股票代號與stock_map裡的股票代號是否一致. 
      * python3 parser.py -t check_board_status -c config.json
      * Possible Error case:
        * There are some missing stock in board=
      * 檢查失敗原因
        * python3 parser.py -t check_board_fail_reason -c config.json
      * 可能導致失敗的結果: 
        * 董監事資料顯示查無資料
        * 董監事資料不繼續公開發行
        * 其他原因: 需再細查      
      
# 成果
https://github.com/starsdog/openGroups.git
