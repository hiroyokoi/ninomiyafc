import streamlit as st
import pandas as pd
import plotly.express as px

# config
st.set_page_config(
    page_title = "NinomiyaFC_Practice_Record",
    page_icon="⚽",
)

# データ読み込み
# 過去の練習記録
data = pd.read_csv('data.csv', encoding = 'cp932', dtype = {'ユーザー名':str, '練習有無':int}, parse_dates = ['練習日'])
# ユーザーマスタ
mst = pd.read_csv('user_mst.csv', encoding = 'cp932')

def main():
    # title入力
    st.title('自主練記録サイト')

    # 入力フォームを作成
    st.subheader('練習データ入力')
    user_name = st.selectbox('名前を選ぶ', mst['選手名'].unique())
    practice_date = st.date_input('練習日')
    practice_done = st.checkbox('練習しましたか？')

    # データフレームに入力データを追加
    if st.button('保存'):
        data.loc[-1] =  {'ユーザー名': user_name, '練習日': pd.to_datetime(practice_date),  '練習有無': practice_done}

    # ユーザー別の練習回数をプロット
    user_counts = data['ユーザー名'].value_counts().reset_index()
    user_counts.columns = ['ユーザー名', '練習回数']
    user_counts = user_counts.sort_values('練習回数', ascending=False)

    # 図の描画画面
    st.subheader("結果")
    plot_type = st.selectbox("表示する図の種類", ["ナンバー1表示", "練習日表示"])
    
    if plot_type == "ナンバー1表示":
        st.subheader('ナンバー1は君だ！')
        fig1 = px.bar(user_counts, x='ユーザー名', y='練習回数')
        fig1.update_layout(xaxis_title='')
        st.plotly_chart(fig1)
        
    elif plot_type == "練習日表示":
        # ユーザー別の練習回数を散布図で表示
        st.subheader('毎日練習してるかな？')
        fig2 = px.scatter(data, x='練習日', y='ユーザー名', size='練習有無')
        fig2.update_xaxes(tickformat='%m/%d')
        fig2.update_layout(xaxis_title='', yaxis_title='')
        st.plotly_chart(fig2)

    
if __name__ == '__main__':
    main()
