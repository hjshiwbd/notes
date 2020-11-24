#  -*- coding:utf-8 -*-  
import logging
import utils
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


class ReportPlayer:
    report = None

    def __init__(self):
        pass

    pass

    def get_db_reportlist(self):
        # sql = "select * from test.wcl_report where title like '2团%' and id between 254 and 277"
        sql = "select * from test.wcl_report where title like '2团%' and report_date > '2020-08-08' limit 15"
        with utils.connect_by_code('test001') as conn:
            return utils.query_list(conn, sql)

    def run(self):
        header = '排名\t名称\t数值\t'
        report_list = self.get_db_reportlist()
        all = []
        for report in report_list:
            self.report = report
            player_list = self.get_player_list()
            total = sum([float(p.player_amount) for p in player_list])
            real_player_list = [p for p in player_list if float(p.player_per_second) > 60]
            count = len(real_player_list)

            player_txt = [header]
            for p in player_list:
                player_one = f"{p.player_rank}\t{p.player_name}\t{p.player_amount}\t{p.player_per_second}"
                player_txt.append(player_one)

            all.append({
                "report_title": self.report.title,
                "txt": "\n".join(player_txt),
                "list": player_list,
                "real_list": real_player_list,
                "total": total,
                "count": count,
                "avg": round(total / count)
            })

        rate = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
        for r in rate:
            self.aaa(r, all)
        pass

    def get_player_list(self):
        sql = 'select * from test.wcl_report_player where report_id = %(report_id)s order by player_rank'
        with utils.connect_by_code('test001') as conn:
            return utils.query_list(conn, sql, {
                "report_id": self.report.id
            })

    def aaa(self, rate, all):
        file = f"d:\\wcl_{rate * 100}%.txt"
        if os.path.exists(file):
            os.remove(file)
        title1 = f'低于全团平均值{rate * 100}%的有'
        for x in all:
            toggle = x['avg'] * rate
            low_p = []
            for p in x['real_list']:
                if float(p.player_amount) < toggle:
                    low_p.append(p.player_name)
            # s1 = f"{x['report_title']}\n{x['txt']}\n{title1}{','.join(low_p)}\n\n\n"
            s1 = f"{x['report_title']}\n{title1}{len(low_p)}人:\n{','.join(low_p)}\n\n\n"
            with open(file, "a+") as io:
                io.write(s1)
