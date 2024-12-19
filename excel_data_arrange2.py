import pandas as pd
from datetime import datetime

# 엑셀 파일 경로
file_path = 'C:\\Daily\\241209_electlink_field_update\\logdata.xlsx'


# 엑셀 데이터 불러오기
df = pd.read_excel(file_path)

# 데이터 확인
print("원본 데이터 미리보기:")
print(df.head())

# NaN 값 제거
df = df.dropna(subset=["SOC", "충전속도"])  # SOC와 충전속도 열에서 NaN 값 제거

# SOC와 충전속도를 숫자로 변환 (문자열로 저장된 숫자를 변환하고 오류 발생 시 NaN 처리)
df["SOC"] = pd.to_numeric(df["SOC"], errors="coerce")
df["충전속도"] = pd.to_numeric(df["충전속도"], errors="coerce")

# NaN 값 제거 (변환 후 NaN 값)
df = df.dropna(subset=["SOC", "충전속도"])

# SOC 구간을 10% 단위로 나누기
bins = range(10, 101, 10)  # 10~100까지 10 단위 구간
labels = [f"{i}~{i+9}%" for i in bins[:-1]]  # 구간 이름
df["SOC_구간"] = pd.cut(df["SOC"], bins=bins, labels=labels, right=False)

# 데이터가 제대로 나누어졌는지 확인
print("SOC 구간 미리보기:")
print(df[["SOC", "SOC_구간", "충전속도"]].head())

# SOC 구간별 평균 충전 속도 계산
result = df.groupby("SOC_구간")["충전속도"].mean().reset_index()

# 결과 출력
print("SOC 구간별 평균 충전속도:")
print(result)

# 현재 시간을 반영한 파일명 생성
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f'C:\\Daily\\SOC_구간별_충전속도_평균_{current_time}.xlsx'

# 결과를 새로운 엑셀 파일로 저장
result.to_excel(output_file_path, index=False)

print(f"결과가 '{output_file_path}'에 저장되었습니다!")
