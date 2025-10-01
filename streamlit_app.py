import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 예제 데이터셋 로드 (타이타닉)
df = sns.load_dataset("titanic")

# 성별에 따른 생존률 막대그래프
st.subheader("🎯 성별에 따른 생존률 시각화")

fig, ax = plt.subplots()
sns.barplot(data=df, x="sex", y="survived", ax=ax)
ax.set_title("성별 생존률")
st.pyplot(fig)

# 나이와 요금의 관계 산점도
st.subheader("🌀 나이와 요금 간의 관계")

fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="age", y="fare", hue="survived", ax=ax2)
ax2.set_title("나이 vs 요금")
st.pyplot(fig2)

# 박스플롯으로 등급별 요금 분포
st.subheader("📦 객실 등급별 요금 분포")

fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x="pclass", y="fare", ax=ax3)
ax3.set_title("등급별 요금 박스플롯")
st.pyplot(fig3)
