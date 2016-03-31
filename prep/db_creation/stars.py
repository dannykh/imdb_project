import requests
import lxml.html
import csv
from prep.IMDB import IMDB
import traceback
import os
import time
from utils import get_sql_id_by_name_in_movie


def get_stars(id):
    page = requests.get("http://www.imdb.com/title/tt" + id).content
    hxs = lxml.html.document_fromstring(page)

    res = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
    if not res:
        res = hxs.xpath('//*[@id="overview-top"]/div[5]/a/span/text()')

    if not res:
        res = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')

    return res


def create_stars_csv(limit=99999):
    conn = IMDB()

    try:
        with open('stars/success.txt', 'rb', 0) as fp:
            done = [line.strip() for line in fp]
    except:
        with open('stars/success.txt', 'wb', 0) as fp:
            done = []
    total, failed, success = 0, 0, 0
    with open("stars/log.txt", 'wb', 0) as log_fp, \
            open("stars/failed.txt", 'wb', 0) as fail_fp, \
            open("stars/stars.csv", 'ab', 0) as stars_fp, \
            open('stars/success.txt', 'ab', 0) as suc_fp:
        csv_writer = csv.writer(stars_fp)
        query = "SELECT id,imdb_id FROM title WHERE NOT imdb_id IS NULL;"
        res = conn.fetch_vec(query)
        ids = [(str(x), str(y)) for x, y in res if str(x) not in done]

        for sql_id, imdb_id in ids:
            if limit <= 0:
                return
            time.sleep(1)
            limit -= 1
            total += 1
            try:
                stars = get_stars(imdb_id)
                if not stars:
                    failed += 1
                    fail_fp.write(sql_id + '\n')
                else:
                    csv_writer.writerow([sql_id] + [stars])
                    suc_fp.write(sql_id + '\n')
                    success += 1
            except Exception, e:
                failed += 1
                fail_fp.write(sql_id + '\n')
                log_fp.write(
                    " AT <{}> : {}  \n {} \n".format(sql_id, e,
                        traceback.format_exc()))


def process_star(conn, mov_id, star, index):
    star_id = get_sql_id_by_name_in_movie(conn, star, mov_id, (1, 2))

    insert_query = "INSERT INTO stars (movie_id,person_id,`index`) " \
                   "VALUES (%s,%s,%s) ;"

    return conn.execute_query(insert_query, mov_id, star_id, index)


def process_movie(conn, imdb_id, stars):
    query = "SELECT id FROM title WHERE imdb_id = %s ;"
    mov_id = conn.fetch_scalar(query, imdb_id)
    for index, star in enumerate(stars):
        process_star(conn, mov_id, star, index + 1)


import re


def fill_stars(stars_csv='http_linkers/stars.csv'):
    conn = IMDB()
    conn.execute_query('DELETE FROM stars;')
    with open(stars_csv, 'rb') as fp, \
            open('stars/db_success.txt', 'wb', 0) as succ_fp, \
            open('stars/db_failed.txt', 'wb', 0) as fail_fp, \
            open('stars/db_log.txt', 'wb', 0) as log_fp:
        reader = csv.reader(fp)
        pr = re.compile(r'.*[\[\]\,].*')
        for row in reader:
            try:
                imdb_id = row[0]
                stars = [x for x in row[1].split('\'') if pr.match(x) is None]
                process_movie(conn, imdb_id, stars)
                succ_fp.write(imdb_id + '\n')
                # print("{} : {} ".format(mov_id, stars))
            except Exception, e:
                fail_fp.write(imdb_id + '\n')
                log_fp.write(
                    " AT <{}> : {}  \n {} \n".format(imdb_id, e,
                        traceback.format_exc()))


def update_stars_csv():
    conn = IMDB()
    query = "SELECT imdb_id FROM title WHERE id = %s ;"
    done = []
    with open('stars/stars_old.csv', 'rb') as old_fp, \
            open('stars/stars.csv', 'wb', 0) as stars_fp:
        reader = csv.reader(old_fp)
        writer = csv.writer(stars_fp)
        for row in reader:
            if row[0] in done:
                continue
            imdb_id = conn.fetch_scalar(query, row[0])
            writer.writerow([imdb_id] + [row[1]])
            done.append(row[0])


if __name__ == "__main__":
    if not os.path.exists('stars/'):
        os.mkdir('stars/')

    fill_stars()

    # update_stars_csv()
