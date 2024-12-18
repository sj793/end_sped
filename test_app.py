import os
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rc, font_manager
from PIL import Image
import requests
from io import BytesIO

# ==== 글꼴 설정 (Linux 환경 호환) ====
font_path = os.path.join("fonts", "NanumGothic.ttf")  # 프로젝트에 포함된 폰트 경로
if os.path.exists(font_path):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
else:
    rc('font', family='Malgun Gothic')  # Windows 환경
plt.rcParams['axes.unicode_minus'] = False

# ==== 이미지 로드 함수 ====
def load_image(image_name):
    return Image.open(os.path.join("images", image_name))

# ==== 페이지 설정 ====
st.set_page_config(page_title="편의점에서 물건 구매하기", layout="wide")

# ==== 선택 메뉴 ====
page = st.sidebar.selectbox(
    "페이지를 선택하세요", 
    ["수업 소개", "편의점 지도", "예산 확인", "마트 예절", "물건 구매", "구매 성공"]
)

# ==== 페이지 별 코드 ====
if page == "수업 소개":
    st.title("편의점에서 물건 구매하기")
    st.write("이 수업은 실제 편의점에서 물건을 구매하며 필요한 사회적 기술과 계산 능력을 익히는 것을 목표로 합니다.")
    st.image(load_image("서울경운학교.png"), caption="서울경운학교", width=600)

elif page == "편의점 지도":
    st.title("종로3가역 주변 편의점 검색")
    st.write("아래 지도에서 종로3가역 주변 편의점을 확인하세요!")
    
    # 네이버 지도 API 설정
    CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
    CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
    latitude, longitude = "37.570028", "126.987080"
    url = f"https://naveropenapi.apigw.ntruss.com/map-static/v2/raster?w=800&h=600&center={longitude},{latitude}&level=14"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLIENT_SECRET,
    }

    # API 호출 및 지도 이미지 출력
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="종로3가역 주변 지도")
    else:
        st.error("지도를 불러올 수 없습니다. API 설정을 확인해주세요.")

elif page == "예산 확인":
    st.title("예산 확인")
    st.write("현재 예산은 총 **10,000원**입니다.")
    st.subheader("예산 구성")
    st.image(load_image("만원.png"), width=200, caption="10,000원")
    st.image(load_image("오천원.png"), width=200, caption="5,000원 X 2")
    cols = st.columns(5)
    for col in cols:
        col.image(load_image("천원.png"), width=200)

elif page == "마트 예절":
    st.title("마트에서 지켜야 할 예절")
    st.subheader("1. 줄을 설 때")
    st.write("다른 사람을 밀거나 끼어들지 않고 차례대로 줄을 섭니다.")
    st.image(load_image("마트예절.png"), caption="마트에서 예절을 지키는 모습", width=800)

elif page == "물건 구매":
    st.title("물건 구매 시뮬레이터")
    items = {
        "가나초콜릿": (2000, "가나초콜릿.png"),
        "코카콜라": (2500, "코카콜라.png"),
        "지우개": (1000, "지우개.png"),
    }
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_items = []
        for item, (price, img_name) in items.items():
            st.image(load_image(img_name), width=200)
            if st.checkbox(f"{item} - {price}원", key=item):
                selected_items.append(item)
            st.markdown("---")
    total = sum(items[item][0] for item in selected_items)
    with col2:
        st.subheader("예산 비교")
        fig, ax = plt.subplots(figsize=(3, 4))
        ax.bar(["현재 금액"], [total], color=["green" if total <= 10000 else "red"])
        ax.axhline(10000, color="blue", linestyle="--", label="예산 (10,000원)")
        ax.legend()
        st.pyplot(fig)
    st.write(f"총 구매 금액: **{total}원**")

elif page == "구매 성공":
    st.title("구매 성공!")
    st.write("축하합니다! 예산 내에서 성공적으로 물건을 구매했습니다.")
    st.image(load_image("참잘했어요.png"), caption="잘했어요! 🎉", width=800)
