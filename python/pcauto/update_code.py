import logging
import math
import utils

mysql_host = 'slave001.yz'
mysql_port = 11502
mysql_user = 'huangj'
mysql_pass = 'hH01KgJMPbVJcYbNAzp@oVe9DdbL4Usg'


class Page:
    page = 1
    page_size = 20
    total_count = 0

    def __init__(self):
        pass

    def get_total_page(self):
        return math.ceil(self.total_count / self.page_size)

    def increase_page(self):
        self.page += 1


def query_sale_list(page):
    start = (page.page - 1) * page.page_size
    sql = "select id,brand_lv1,brand_lv2,code from test.vehicle_sales_pcauto where code is null limit %(limit)s, %(offset)s"
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        return utils.query_list(conn, sql, {'limit': start, 'offset': page.page_size})


def query_sale_list_total():
    sql = "select count(*) cc from test.vehicle_sales_pcauto where code is null"
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        return utils.query_one(conn, sql)


def query_vehcile_list():
    sql = "select * from test.vehicle_info"
    with utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass) as conn:
        return utils.query_list(conn, sql)


def update_sale_code(conn, code, lv1, lv2):
    sql = ("update test.vehicle_sales_pcauto set code = %(code)s where brand_lv1 = %(brand_lv1)s "
           "and brand_lv2 = %(brand_lv2)s")
    return utils.update(conn, sql, {'code': code, 'brand_lv1': lv1, 'brand_lv2': lv2})


def run():
    # rank表里面拿到brandlv1和lv2,查info表里的code,回写rank表
    page = Page()
    page.page_size = 5000

    v = query_sale_list_total()
    page.total_count = v.cc

    info_list = query_vehcile_list()

    conn = utils.connect(mysql_host, mysql_port, mysql_user, mysql_pass)

    while page.page <= page.get_total_page():
        sale_list = query_sale_list(page)
        print(f'{page.page}/{page.get_total_page()}')
        page.increase_page()

        def is_lv1_and_lv2_eq(info, sale):
            return info.brand_lv1 == sale.brand_lv1 and info.brand_lv2 == sale.brand_lv2

        for i in range(len(sale_list)):
            sale = sale_list[i]
            if sale.code is not None:
                continue
            lv1 = sale.brand_lv1
            lv2 = sale.brand_lv2
            vv = list(filter(lambda info: is_lv1_and_lv2_eq(info, sale), info_list))
            if len(vv) == 0:
                print(f'未找到:{lv1}-{lv2}')
                continue
            if len(vv) > 1:
                raise f'info表有重名:{lv1}-{lv2}'
            n = update_sale_code(conn, vv[0].code, lv1, lv2)
            print(f'update for {lv1}-{lv2}: {n}, info:{i}/{len(sale_list)}, page:{page.page}/{page.get_total_page()}')

    conn.close()
    pass


if __name__ == '__main__':
    run()
