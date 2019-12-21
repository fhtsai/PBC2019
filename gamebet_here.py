class gamebet():
    """
    def odds 需要輸入雙方隊伍名字
    return 賠率清單，單元數固定
    [['單雙', '單', 1.75, '雙', 1.75],
     ['大小(總分)', '大於X分', 1.75, '小於X分', 1.75],
     ['不讓分', 'A隊名', A賠率, 'B隊名', B賠率]]
    """
    def odds(self, team_name_A, team_name_B):
        print("***calculating odds...")
        data_list = []
        
        #獲得雙方隊伍勝率與平均得分
        print("getting team", team_name_A, "stats...")
        teamA = Team(team_name_A)
        teamA.get_info() #勝率是int(teamA.info[4])
        self.win_oddsA = (float(teamA.info[4][:(len(teamA.info[4])-1)]) / 100)
        teamA.get_game() #平均得分是teamA.game[(len(teamA.game) - 1)]
        self.score_A = teamA.game[(len(teamA.game) - 1)]
        
        print("getting team", team_name_B, "stats...")        
        teamB = Team(team_name_B)
        teamB.get_info() #勝率B是int(teamB.info[4])
        self.win_oddsB = (float(teamB.info[4][:(len(teamB.info[4])-1)]) / 100)
        teamB.get_game() #平均得分是teamB.game[(len(teamB.game) - 1)]
        self.score_B = teamB.game[(len(teamB.game) - 1)]
        
        """
        賠率公式：
        1. 單雙：雙方賠率都是1.75
        2. 大小(總分)：
        3. 不讓分：需判斷勝率/平均總分，決定賠率
        簡易版本：勝率對應好壞狀態，若A好B壞，則A贏；反之則B贏。若A好B好，A壞B壞，則判斷平均得分。
        若平均得分相差小於9分，則判定勝率各半。
        勝率倒數為賠率，Cap最高是3.75倍，最低是1.15倍
        """
        
        #單雙
        data_list.append(['單雙', '單', 1.75, '雙', 1.75])
        
        #大小
        scoresum = teamA.game[(len(teamA.game) - 1)] + teamB.game[(len(teamB.game) - 1)]
        scoresum = int(scoresum) + 0.5 #確保大小是以.5結尾
        data_list.append(['大小(總分)', ('大於' + str(scoresum)), 1.75,
                          ('小於' + str(scoresum)), 1.75])
        
        #不讓分
        teamA_odds = self.win_oddsA * (1 - self.win_oddsB)
        teamB_odds = self.win_oddsB * (1 - self.win_oddsA)
        
        if abs(self.score_A - self.score_B) <= 9:
            teamA_odds += ((1 - teamA_odds) - teamB_odds) / 2
            teamB_odds += ((1 - teamA_odds) - teamB_odds) / 2 

        elif self.score_A > self.score_B:
            teamA_odds += (1 - teamA_odds - teamB_odds)

        elif self.score_A < self.score_B:
            teamB_odds += (1 - teamA_odds - teamB_odds)
        
        print('win odds:', teamA_odds, teamB_odds)

        if teamA_odds != 0 and teamB_odds != 0: #判斷Cap
            teamA_odds = round((1 / teamA_odds), 2)
            teamB_odds = round((1 / teamB_odds), 2)
            
            teamA_odds = 3.75 if (teamA_odds > 3.75) else teamA_odds
            teamA_odds = 1.15 if (teamA_odds < 1.15) else teamA_odds
            teamB_odds = 3.75 if (teamB_odds > 3.75) else teamB_odds
            teamB_odds = 1.15 if (teamB_odds < 1.15) else teamB_odds
    
        else: #如果有一方勝率為0時，則直接給上下Cap最大賠率
            if teamA_odds == 0:
                teamA_odds = 3.75
                teamB_odds = 1.15
                
            elif teamB_odds == 0:
                teamA_odds = 1.15
                teamB_odds = 3.75
        
        print('bet odds for 不讓分:', teamA_odds, teamB_odds)
        
        data_list.append(['不讓分', team_name_A, teamA_odds, team_name_B, teamB_odds])
        
        return data_list
    
    """
    def get_bettingA(final_g) ，需要輸入當日賽程清單
    return list：一場賽事回傳一個完整賠率清單
    舉例：[['時間', 'A隊', 'B隊', '地點', [[單雙], [大小], [不讓分]]],
           ['時間', 'C隊', 'D隊', '地點', [[單雙], [大小], [不讓分]]]...]
    
    A版本使用For迴圈一個一個計算，算出全部的賠率，非常耗時間。
    """
    def get_bettingA(self, final_g):
        #先得到當日賽事資訊
        data_list = []
        
        #Team與bet對照隊名用
        teamnamedict = {"塞爾蒂克": "波士頓塞爾蒂克", "公牛": "芝加哥公牛", 
                    "老鷹": "亞特蘭大老鷹", "籃網": "布魯克林籃網", 
                    "騎士": "克里夫蘭騎士", "黃蜂": "夏洛特黃蜂", "尼克": "紐約尼克",
                    "活塞": "底特律活塞", "熱火": "邁阿密熱火", "76人": "費城76人",
                    "溜馬": "印第安納溜馬", "魔術": "奧蘭多魔術", "暴龍": "多倫多暴龍", 
                    "公鹿": "密爾瓦基公鹿", "巫師": "華盛頓巫師", "金塊": "丹佛金塊", "勇士": "金州勇士", 
                    "獨行俠": "達拉斯獨行俠", "灰狼": "明尼蘇達灰狼", "快艇": "洛杉磯快艇",
                    "火箭": "休士頓火箭", "雷霆": "奧克拉荷馬城雷霆", "湖人": "洛杉磯湖人", 
                    "灰熊": "曼菲斯灰熊", "拓荒者": "波特蘭拓荒者", "太陽": "鳳凰城太陽", 
                    "鵜鶘": "紐奧良鵜鶘", "爵士": "猶他爵士", "國王": "沙加緬度國王", "馬刺": "聖安東尼奧馬刺"}
        
        #for迴圈判定賠率
        for i in range(len(final_g)):
            data_list.append(final_g[i])
            print('***Getting game of', teamnamedict[final_g[i][1]],"vs.", teamnamedict[final_g[i][2]])
            odds_list = self.odds(teamnamedict[final_g[i][1]], teamnamedict[final_g[i][2]])
            data_list[i].append(odds_list)
            print('***Check list', data_list[i])
            print()
            print()
        
        return data_list

    #判斷下幾注，賠率
    """
    三種寫法分別對應不同的結果?
    """
    #def go_bet(self):
        
    
    #下注
    """
    def gobet 需要輸入一個清單：['時間', 'A隊', 'B隊', '地點', '賭法', '下幾柱']
    - 從帳戶扣除應繳金額
    - 新增一筆交易資料，此交易資料會是一個清單：
      ['時間', 'A隊', 'B隊', '地點', '賭法', '下幾柱', '輸/贏/未交割', 盈虧]
    - 回傳
    """
    #def confirm_bet(self, bet):
        #需要一個Check Balance的函數
        
        
        #從帳戶扣取應繳金額
        #新增一筆交易資料
        
        
    #結算
    """
    def clearance 不須輸入
    每次開檔時需跑這個函數
    - 從帳戶資料中讀取是否有未交割的賭注
    - 從歷史資料中獲得結果
    - 更新帳戶餘額與交易紀錄
    """   
    #def clearance(self): 
