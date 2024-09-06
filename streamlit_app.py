import streamlit as st
import pandas as pd

# ตั้งค่า Page
st.set_page_config(page_title="Part Evaluation", layout="wide")

# อัปโหลดไฟล์ Excel
uploaded_file = st.file_uploader("กรุณาอัปโหลดไฟล์ Excel ที่มีข้อมูลอะไหล่", type=["xlsx"])

if uploaded_file is not None:
    # โหลดข้อมูลจากไฟล์ Excel ที่อัปโหลด
    spare_parts_df = pd.read_excel(uploaded_file)

    # รักษาสถานะปัจจุบันของ index ใน SessionState
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    # ดึงข้อมูล part ปัจจุบัน
    current_part = spare_parts_df.iloc[st.session_state.current_index]

    # Title
    st.title('Part Importance Evaluation System')

    # แสดงข้อมูล Part ปัจจุบัน
    st.write(f"**Part Number:** {current_part['Part Number']}")
    st.write(f"**Part ID:** {current_part['Part ID']}")
    st.write(f"**Description:** {current_part['Description']}")

    # ส่วนที่ 1: การให้คะแนนในแต่ละเกณฑ์
    st.subheader('กรุณาเลือกคะแนนให้กับอะไหล่ตามเกณฑ์ต่อไปนี้:')

    # เกณฑ์ที่ 1: Safety Impact
    st.subheader('ผลกระทบต่อความปลอดภัย (Safety Impact)')
    safety_impact = st.radio('คะแนน', ['Critical', 'Important', 'Standard'], key=f'safety_{st.session_state.current_index}')

    # เกณฑ์ที่ 2: Operational Impact
    st.subheader('ผลกระทบต่อการดำเนินงาน (Operational Impact)')
    operational_impact = st.radio('คะแนน', ['Critical', 'Important', 'Standard'], key=f'operational_{st.session_state.current_index}')

    # เกณฑ์ที่ 3: Availability of Substitutes
    st.subheader('ความพร้อมในการทดแทน (Availability of Substitutes)')
    substitute_impact = st.radio('คะแนน', ['Critical', 'Important', 'Standard'], key=f'substitute_{st.session_state.current_index}')

    # เกณฑ์ที่ 4: Usage Frequency
    st.subheader('ความถี่ในการใช้งาน (Usage Frequency)')
    usage_impact = st.radio('คะแนน', ['Critical', 'Important', 'Standard'], key=f'usage_{st.session_state.current_index}')

    # คำนวณคะแนนรวม
    safety_score = 5 if safety_impact == 'Critical' else 3 if safety_impact == 'Important' else 1
    operational_score = 5 if operational_impact == 'Critical' else 3 if operational_impact == 'Important' else 1
    substitute_score = 5 if substitute_impact == 'Critical' else 3 if substitute_impact == 'Important' else 1
    usage_score = 5 if usage_impact == 'Critical' else 3 if usage_impact == 'Important' else 1

    total_score = safety_score + operational_score + substitute_score + usage_score
    st.write(f'คะแนนรวม: {total_score}')

    # เปรียบเทียบกับค่าหน้ำนัก
    st.subheader('เปรียบเทียบกับค่าน้ำหนัก')
    if total_score >= 15:
        weight_factor = 1.5
        importance = 'ความสำคัญสูง'
    elif total_score >= 10:
        weight_factor = 1.2
        importance = 'ความสำคัญปานกลาง'
    else:
        weight_factor = 1.0
        importance = 'ความสำคัญต่ำ'

    st.write(f'ค่าหน้ำนัก: {weight_factor}')
    st.write(f'แสดงถึงความสำคัญ: {importance}')

    # เมื่อกดปุ่ม Submit ให้บันทึกข้อมูล
    if st.button('Submit'):
        # สร้าง DataFrame สำหรับบันทึกข้อมูล
        df = pd.DataFrame({
            'Part Number': [current_part['Part Number']],
            'Part ID': [current_part['Part ID']],
            'Description': [current_part['Description']],
            'Safety Impact': [safety_impact],
            'Operational Impact': [operational_impact],
            'Substitutes Availability': [substitute_impact],
            'Usage Frequency': [usage_impact],
            'Total Score': [total_score],
            'Weight Factor': [weight_factor],
            'Importance': [importance]
        })

        # บันทึกลงในไฟล์ CSV (ถ้าไฟล์มีอยู่แล้ว จะเพิ่มข้อมูลต่อท้าย)
        df.to_csv('part_evaluation_data.csv', mode='a', header=False, index=False)

        st.success('ข้อมูลของคุณถูกบันทึกเรียบร้อยแล้ว')

    # ปุ่ม Next สำหรับไปยังรายการถัดไป
    if st.button('Next'):
        # เพิ่ม index ไปยังรายการถัดไป
        st.session_state.current_index += 1

        # ถ้าประเมินครบทุก part แล้ว ให้จบโปรแกรม
        if st.session_state.current_index >= len(spare_parts_df):
            st.write("การประเมินครบแล้ว ขอบคุณ!")
            st.session_state.current_index = 0  # เริ่มใหม่จาก index แรกถ้าต้องการ
        else:
            # ใช้วิธีการรีเซ็ตค่าโดยการ refresh ด้วย `st.experimental_set_query_params`
            st.experimental_set_query_params(next_part=st.session_state.current_index)
