from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# 맨위에 있는 게시글에 대해서만 반응하는 프로그램

# 네이버 계정
userID = 'er_ys'

# 네이버 pw
userPW = '!ㅁㅁㅁㅁ'

# 마지막 게시글
last_title = '시작'

# 작성자
# 작성자 상관없는 경우 ''으로
like_name = '동검'

# 내용
comment = 'ㅂ'

# 반복 횟수
# ex) 몇개의 게시글에 남길거냐
maxCnt = 20


# 카페 URL
# cafeUrl = 'https://cafe.naver.com/blackhmq8n?iframe_url=/ArticleList.nhn%3Fsearch.clubid=30930879%26search.boardtype=L'
# 동검
cafeUrl = 'https://cafe.naver.com/donggumdo?iframe_url=/ArticleList.nhn%3Fsearch.clubid=29060781%26search.boardtype=L'
cnt = 1


# 웹 드라이버 경로 설정
driver = webdriver.Chrome()

# 1) 네이버 카페 로그인
driver.get('https://nid.naver.com/nidlogin.login')
elem_login = driver.find_element("id", 'id')
elem_login.clear()
elem_login.send_keys(userID)
elem_login = driver.find_element("id", 'pw')
elem_login.clear()
elem_login.send_keys(userPW)
elem_login.submit()

# 1-1) 로그인 화면 나가기
while True:
    time.sleep(5)
    if driver.current_url != 'https://nid.naver.com/nidlogin.login':
        print("로그인 성공")
        break;


# 2) 네이버 카페 URL 접속
while cnt <= maxCnt:
    print('마지막 게시글  :: ', last_title)
    driver.get(cafeUrl)
    try:
        driver.switch_to.frame("cafe_main")
    except:
        continue


    elements = driver.find_elements(By.CLASS_NAME, 'article-board');
    # 0 = 공지
    # 1 = 전체
    if len(elements) > 1:
        element = elements[1]
    else:
        element = elements[0]

    titles = element.find_elements(By.CLASS_NAME, 'article')
    names = element.find_elements(By.CLASS_NAME, 'td_name')

    if titles[0].text != last_title and like_name in names[0].text:
        print('새로운 게시글이 생겼음 , 프로세스 진행  : ', titles[0].text)
        print('시작시간 : ', datetime.now())
        new_title = titles[0].text
        driver.get(titles[0].get_attribute('href'))
        try :
            driver.switch_to.frame("cafe_main")
        except:
            continue

        # 댓글 쓰기 프로세스 진행
        while True:
            try:
                WebDriverWait(driver,0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment_inbox_text')))
                inputBox = driver.find_element(By.CLASS_NAME, 'comment_inbox_text')
                inputBox.send_keys(comment)
                butten = driver.find_element(By.CLASS_NAME, 'register_box');
                butten.click()
                last_title = new_title
                break;

            except:
                continue

    else:
        print('새로운 글이 없습니다');


time.sleep(15)
