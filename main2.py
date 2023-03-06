from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 마지막으로 설정한 게시글에 대해 순차적으로 모든 댓글 남기기

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

cafeUrl = 'https://cafe.naver.com/blackhmq8n?iframe_url=/ArticleList.nhn%3Fsearch.clubid=30930879%26search.boardtype=L'
cnt = 1


# 웹 드라이버 경로 설정
driver = webdriver.Chrome()

# 네이버 카페 로그인
driver.get('https://nid.naver.com/nidlogin.login')
elem_login = driver.find_element("id", 'id')
elem_login.clear()
elem_login.send_keys(userID)
elem_login = driver.find_element("id", 'pw')
elem_login.clear()
elem_login.send_keys(userPW)
elem_login.submit()

while True:
    time.sleep(5)
    if driver.current_url != 'https://nid.naver.com/nidlogin.login':
        print("로그인 성공")
        break;


# 네이버 카페 URL 접속
# for a in range(1):
while cnt <= maxCnt:
    print('마지막 게시글  :: ', last_title)
    driver.get(cafeUrl)
    time.sleep(0.05)
    driver.switch_to.frame("cafe_main")
    elements = driver.find_elements(By.CLASS_NAME, 'article-board');
    # 0 = 공지
    # 1 = 전체
    if len(elements) > 1:
        element = elements[1]
    else:
        element = elements[0]

    titles = element.find_elements(By.CLASS_NAME, 'article')
    names = element.find_elements(By.CLASS_NAME, 'td_name')

    new_title = []
    new_url = []
    for i in range(len(titles)):
        if titles[i].text == last_title and like_name in names[i].text:
            break
        else:
            new_title.append(titles[i].text)
            new_url.append(titles[i].get_attribute('href'))

    print(new_title)

    if len(new_title) > 0:
        print('새글 ',len(new_title),'개')
        for i in range(len(new_title)-1, -1, -1):
            print(new_title[i]);
            last_name = new_title[i]
            driver.get(new_url[i])
            time.sleep(0.05)
            driver.switch_to.frame("cafe_main")
            # 댓글 쓰기 프로세스 진행
            try:
                WebDriverWait(driver, 0.7).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment_inbox_text')))
                inputBox = driver.find_element(By.CLASS_NAME, 'comment_inbox_text')
                inputBox.send_keys(comment)
                butten = driver.find_element(By.CLASS_NAME, 'register_box');
                butten.click()
                last_title = new_title[i]
                cnt += 1
            except:
                print('에러 : 재시도')
            finally:
                time.sleep(0.75)
    else:
        print('새로운 글이 없습니다.')






time.sleep(15)
