import streamlit as st
import pandas as pd

from time import sleep


def email_send(row: list): 
    print(row[0], row[1], row[2])
    sleep(0.3) 

st.title('Perking邮件推送服务')

email_subject = st.text_area(label='邮件主题', placeholder='在此输入邮件主题')
email_content = st.text_area(label='邮件内容', height=500, placeholder='在此输入邮件内容')
receiver = st.text_input(label='回复信箱', placeholder='邮件推送后收到对方回复的邮箱')

st.divider()

xlsx_file = st.file_uploader('上传xlsx文件', type='xlsx')
st.markdown('**xlsx文件格式务必如下图所示**')
st.image('xlsx_format.png')

st.divider()

if xlsx_file:
    df = pd.read_excel(xlsx_file)
    st.dataframe(df)

    send_submit_button = st.button(label='开始推送邮件')

    if send_submit_button:
        progress_text = '正在推送邮件...'
        email_bar = st.progress(0, text=progress_text)
        css = '''
<style>
    [data-testid="stSidebar"]{
        min-width: 500px;
        max-width: 600px;
    }
</style>
'''
        st.markdown(css, unsafe_allow_html=True)

        for (step, (_, row)) in enumerate(df.iterrows(), start=1):
            email_send(row)
            if step % 2 == 0:
                st.sidebar.success(f'发送邮件至{row[2]}成功!', icon="✅")
            else:
                st.sidebar.warning(f'发送邮件至{row[2]}失败!', icon="⚠️")
            email_bar.progress(step*(100/df.shape[0])/100, text=progress_text)

        st.header('邮件推送完成')
        st.balloons()