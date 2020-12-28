#  -*- coding:utf-8 -*-  
import logging
import utils

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


class ReportAward:
    report = None
    report_id = 0
    dmg_classes = ['hunter', 'mage', 'rogue', 'warlock', 'warrior']

    def __init__(self, report_id):
        self.report_id = report_id
        pass

    def run(self):
        sql = f"""
select t.name,t.class,t1.player_amount from wcl_player  t join 
(select  * from wcl_report_player  where report_id =428 and report_type = 'dmg') t1 on t.`name` = t1.player_name
where t.class = 'rogue'
"""
        with utils.connect_by_code('test001') as conn:
            return utils.query_list(conn, sql)
        pass
