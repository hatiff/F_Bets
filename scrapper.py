import re
import pandas as pd
import os


class Scrapper():
    def __init__(self):
        self.name = None
        self.name_list = []
        self.team_1 = None
        self.team_1_list = []
        self.team_1_goal = None
        self.team_1_goal_list = []
        self.team_2 = None
        self.team_2_list = []
        self.team_2_goal = None
        self.team_2_goal_list = []
        self.win_1 = None
        self.win_1_list = []
        self.win_2 = None
        self.win_2_list = []
        self.time = None
        self.time_list = []
        self.even = None
        self.even_list = []
        self.score = None
        self.score_list = []
        self.coef_w_1 = None
        self.coef_w_1_list = []
        self.coef_w_2 = None
        self.coef_w_2_list = []
        self.coef_even = None
        self.coef_even_list = []
        self.prev_string = 'nothing_new'
        self.string = 'none'


    def _reset(self):
        self.team_1 = None
        self.team_1_goal = None
        self.team_2 = None
        self.team_2_goal = None
        self.time = None
        self.even = None
        self.coef_w_1 = None
        self.coef_w_2 = None
        self.coef_even = None
        self.prev_string = 'nothing_new'
        self.string = 'none'


    def add_to_lists(self):
        try:
            int(self.team_1_goal)
            int(self.team_2_goal)
            float(self.coef_w_1)
            float(self.coef_w_2)
            float(self.coef_even)
        except:
            return "ok"
            #print(self.team_1)
            #print(self.team_1_goal)
            #print(self.team_2)
            #print(self.time)
            #print(self.name)
            #print(self.coef_w_1)
            #print(self.coef_even)
            #print(self.coef_w_2)
            #print("______________________")
        self.team_1_list.append(self.team_1)
        self.team_1_goal_list.append(int(self.team_1_goal))
        self.team_2_list.append(self.team_2)
        self.team_2_goal_list.append(int(self.team_2_goal))
        self.time_list.append(self.time)
        self.name_list.append(self.name)
        self.coef_w_1_list.append(float(self.coef_w_1))
        self.coef_w_2_list.append(float(self.coef_w_2))
        self.coef_even_list.append(float(self.coef_even))




    
    def add_to_sheets(self):
        df = pd.DataFrame({'tournament': self.name_list,
                            'team_1': self.team_1_list,
                           'team_1_goals': self.team_1_goal_list,
                          'team_2': self.team_2_list,
                          'team_2_goals': self.team_2_goal_list,
                          'time': self.time_list,
                          'coef_w_1': self.coef_w_1_list,
                          'coef_w_2': self.coef_w_2_list,
                          'coef_even': self.coef_even_list})
        return df


    def logic(self):
        if not self.time:
            re_out = re.findall('\d{2}:\d{2}', self.string)
            if len(re_out) != 0:
                self.time = re_out[0]

        elif not self.team_1:
             self.team_1 = self.string

        elif not self.team_1_goal:
            self.team_1_goal = self.string

        elif not self.team_2:
            self.team_2 = self.string

        elif not self.team_2_goal:
            self.team_2_goal = self.string
    
        elif not self.coef_w_1:
            if self.string.strip()[0] == '-' or 'none' in self.string:
                 self._reset()
                 return 'ok'
            self.coef_w_1 = self.string
            #re_out = re.findall(r"\b\d{1,2}.\d{1,2}\b", self.string)
            #if len(re_out) != 0:
                #self.coef_w_1 = re_out[0]
        
        elif not self.coef_even:
            if self.string.strip()[0] == '-':
                 self._reset()
            #re_out = re.findall(r"\b\d{1,2}.\d{1,2}\b", self.string)
            #if len(re_out) != 0:
             #   self.coef_even = re_out[0]
            self.coef_even = self.string
        
        elif not self.coef_w_2:
            #re_out = re.findall(r"\b\d{1,2}.\d{1,2}\b", self.string)
            #if len(re_out) != 0:
             #   self.coef_w_2 = re_out[0]
            self.coef_w_2 = self.string
            self.add_to_lists()
            self._reset()
        
        self.prev_string = self.string


    def scrapp_file(self, file):
        raw_text = open(file, 'r')
        for row in raw_text:
            if len(row.strip()) == 0:
                continue
            else:
                self.string = row
                self.logic()

        return self.add_to_sheets()
    
    def scrapp_multi_files(self, folder ):
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                self.name = file
                with open(file_path, 'r') as myfile:
                    for row in myfile:
                        if len(row.strip()) == 0:
                            continue
                        else:
                            row = row.replace('\n', '')
                            self.string = row
                            self.logic()

        return self.add_to_sheets()

        
    def scrapp_text(self, raw_text):
        for row in raw_text:
            if len(row.strip()) == 0:
                continue
            else:
                self.string = row
                self.logic()

        return self.add_to_sheets()



if __name__=='__main__':
    scrapper = Scrapper()
    data_pd = scrapper.scrapp_from_file("Bets 26-27.02.txt")
