import requests
from bs4 import BeautifulSoup
import re
import csv
import logging

logging.basicConfig(level=logging.DEBUG, filename='log.txt',
                    format=' %(asctime)s - %(levelname)s - %(message)s')

BASE_URL = 'https://www.apt2you.com/'   # 최상위 도메인
LIST_PAGE = 'houseSaleSimpleInfo.do'  # 아파트 청약 리스트 페이지
DETAIL_PAGE = 'houseSaleDetailInfo.do?manageNo='   # 청약 세부 정보 페이지


def create_list_from_table(table_tag):

    # 2중 리스트 생성
    apts = []

    # 헤더에 해당하는 1번째 로우 작성
    headers = []
    headers_tags = table_tag.find('tr')
    for th_tag in headers_tags.find_all('th'):
        headers.append(th_tag.text.strip())
    apts.append(headers)

    # 아파트 레코드 작성
    for tr_tag in table_tag.find_all('tr'):
        apt = []
        for td_tag in tr_tag.find_all('td'):
            # 공백 제거
            content = re.sub('[\t\r\n]', '', td_tag.text.strip())
            if td_tag.a:
                # 링크 추출
                link = BASE_URL + DETAIL_PAGE + td_tag.a.get('onclick')[16:26]
                content = content + '(' + link + ')'

            apt.append(content)

        if not apt:
            continue
        apts.append(apt)

    # logging.debug(apts)
    return apts


def create_csv_file(gifts, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for i in gifts:
            writer.writerow(i)


def main():
    logging.debug('Start of program')

    res = requests.get(BASE_URL + LIST_PAGE)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 테이블 태그 확보
    table_tag = soup.find("table", {"class": "tbl_default sortable"})
    logging.debug('Start of program')

    apts = create_list_from_table(table_tag)
    create_csv_file(apts, 'apts.csv')

    logging.debug('End of program')


if __name__ == '__main__':
    main()
