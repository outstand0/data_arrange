import pandas as pd

# 엑셀 파일을 불러옵니다.
file_path = 'C:\\Daily\\241118_electlink_secc_log_autosave\\electlink_raw_data_241105\\시그넷신규200kw_1001to1024_OCT_mod.xlsx'
df = pd.read_excel(file_path)

# 충전 ID별로 그룹화하고, 각 그룹의 첫 번째와 마지막 행을 추출합니다.
result = df.groupby('충전ID').agg(['first', 'last']).reset_index()

# 결과를 엑셀 파일로 저장하거나 출력합니다.
result.columns = [f'{col[0]}_{col[1]}' for col in result.columns]  # 컬럼명 정리
result.to_excel('C:\\Daily\\241118_electlink_secc_log_autosave\\electlink_raw_data_241105\\충전ID_시작_끝.xlsx', index=False)

