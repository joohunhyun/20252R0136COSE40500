# ---------- import libraries ----------

# http request를 위한 라이브러리
import requests
# 정규식을 사용하기 위한 라이브러리
import re
# arvix element tree를 사용하기 위한 라이브러리
import xml.etree.ElementTree as ET
# 웹페이지 파싱을 위한 라이브러리
from bs4 import BeautifulSoup
# fallback logic을 위한 라이브러리
from readability import Document
# 시간 측정용 라이브러리
import time

# ---------------------------------------


def get_arxiv_abstract(arxiv_id):
    """
    arxvix.org에서 arxiv_id에 해당하는 논문의 초록을 가져오는 함수
    """
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
        abstract = root.find(".//arxiv:summary", ns).text
        return abstract.strip()
    else:
        return fallback_extraction(url)

def handle_arxiv(url):
    """
    arxiv.org 사이트의 URL을 처리하는 함수. 
    주헌 : 별도의 핸들러가 필요한 이유는 arvix_id를 추출해서 export.arxiv.org API를 사용하여 논문의 초록을 가져오도록 하기 위함입니다.
    """
    arxiv_id = url.rstrip('/').split('/')[-1]
    return get_arxiv_abstract(arxiv_id)