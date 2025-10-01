import streamlit as st

st.title("🎈 Sodam first app")

st.write("반갑습니다. 저는 1-5 현하윤입니다.")
st.success('배고파요')
st.info('으아아아아 저녁ㄱㄱㄱㄱㄱ')
st.image("https://pbs.twimg.com/media/GdpDqQZWMAAFOP6.jpg:large")

st.markdown("---")

st.markdown("오. 내 *친구*.")

st.title("뭐요")
st.header("착 한 아 이")
st.subheader("hehehehehe")

st.markdown("---")

st.link_button("ddd", "https://youtu.be/Fokx686r55I")

st.code("""
import streamlit as st
st.title('Hello World')
""", language="python")

st.link_button("[꾸몽] 팀샐러드 화면 조정", 'https://youtu.be/S_UtMc-gYeE?si=xkQ58GNhYDF4qbLt')


st.markdown('---')

tab1, tab2 = st.tabs(['탭1','탭2'])

with tab1:
    st.write("탭1")

    color = st.selectbox("좋아하는 색을 선택하세요", ["빨강", "초록", "파랑"])
    st.write("선택한 색상:", color)

    if color == "빨강":
        st.error("빨강")
    
    subjects = st.multiselect("관심 있는 과목을 선택하세요", ["수학", "영어", "과학"])
    st.write("선택한 과목:", subjects)

with tab2:
    st.write("귀하의 컴퓨터를 털어가는 것에 동의하십니까?")

    agree = st.checkbox("위 조건에 동의합니다")
    if agree:
        st.write("감사합니다! 계속 진행합니다.")

    gender = st.radio("옆 사람의 성별을 선택하세요", ["남성", "여성", "사람이 아닙니다"])
    st.write("선택한 성별:", gender)






st.sidebar.title("사이드바")
st.sidebar.write("hi")
st.sidebar.write("hehehe")

st.markdown('---')

age = st.number_input("나이를 입력해주세요", step=1)

st.write(2026-age)
st.write(f"{2026-age}년도에 태어나셨군요!")

with st.expander("ℹ️ 자세한 설명 보기"):
    st.write("여기에 상세 설명이나 보조 정보를 넣을 수 있습니다.")








level = st.slider("난이도를 선택하세요", 1, 10, 1)
st.write("선택한 난이도:", level)

date = st.date_input("날짜를 선택하세요")
st.write("선택한 날짜:", date)




