import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlitアプリの設定
st.set_page_config(page_title="学習時間調査分析")

# アプリケーションのタイトルと説明
st.title("学習時間調査分析")
st.caption("Created by Dit-Lab.(Daiki Ito)")

# ファイルアップローダー
uploaded_file = st.file_uploader('Excelファイルをアップロードしてください', type=['xlsx'])

# データフレームの作成
df = None

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # 全ての列が空の列を削除
    empty_columns = df.columns[df.isna().all()].tolist()
    df = df.dropna(axis=1, how='all')
    
    st.write(df.head())
    
    st.subheader('分析データの選択')

    # カテゴリ変数の抽出
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    # 数値変数の抽出
    numerical_cols = df.select_dtypes(exclude=['object', 'category']).columns.tolist()

    # 学年・クラスデータの選択
    st.subheader("学年・クラスデータの選択")
    
    # カテゴリデータがない場合の処理
    if len(categorical_cols) == 0:
        st.error('カテゴリ（文字列）データがありません')
        st.stop()
    
    grade = st.multiselect('学年を示す列を選択してください', categorical_cols,max_selections=1)
    group = st.multiselect('クラスを示す列を選択してください', categorical_cols,max_selections=1)
      
    # 数値データがない場合の処理
    if len(numerical_cols) == 0:
        st.error('数値データがありません')
        st.stop()

    # 分析用データの抽出
    st.subheader("平日の学習時間データの選択")
    weekdays = st.multiselect('分析に使用する平日の学習時間データを選択してください', numerical_cols)
    st.subheader("休日の学習時間データの選択")
    holidays = st.multiselect('分析に使用する休日の学習時間データを選択してください', numerical_cols)

    # 選択したデータのみを抽出し、表示する
    temp_df = df[[*grade, *group, *weekdays, *holidays]]
    
    #temp_dfをセッションに保存
    st.session_state.temp_df = temp_df
    
    # 分析用データの表示
    st.subheader("分析用データ")
    st.write(temp_df)
    
    # 分析実行ボタンの表示
    if st.button('分析実行'):
        st.subheader("分析結果")
        # 学年ごとの平日・休日の学習時間ｗの平均値を算出
        mean_df = temp_df.groupby(grade).mean()
        st.write(mean_df)