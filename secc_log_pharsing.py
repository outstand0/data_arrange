import re
import csv

# 파일 경로 설정
file_path = r"C:\\Daily\\241209_electlink_field_update\\logs\\2024-12-11-10-51-53_SECC.log"
output_path = r"C:\\Daily\\241209_electlink_field_update\\logs\\parsed_data.csv"

# 결과 저장을 위한 리스트 초기화
parsed_data = []

# 로그 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()  # 파일을 한 줄씩 읽어 리스트로 저장

# 데이터 세트 추출 로직
for i in range(len(lines) - 1):  # 현재 줄과 다음 줄을 함께 처리하기 위해 범위 설정
    current_line = lines[i].strip()  # 현재 줄
    next_line = lines[i + 1].strip()  # 다음 줄

    # `.req` 라인 처리
    if "currentdemand.req" in current_line.lower():
        # 다음 줄에서 `soc`와 `tgtA` 추출
        soc_match = re.search(r"soc=(\d+)", next_line)
        tgtA_match = re.search(r"tgtA\((\d+),", next_line)

        soc = int(soc_match.group(1)) if soc_match else None
        tgtA = float(tgtA_match.group(1)) / 10 if tgtA_match else None

    # `.res` 라인 처리
    if "currentdemand.res" in current_line.lower():
        # 다음 줄에서 `preA`와 `preV` 추출
        preA_match = re.search(r"preA\((\d+),", next_line)
        preV_match = re.search(r"preV\((\d+),", next_line)

        preA = float(preA_match.group(1)) / 10 if preA_match else None
        preV = int(preV_match.group(1)) / 10 if preV_match else None

        # `soc`, `tgtA`, `preA`, `preV`가 모두 존재할 때 데이터 추가
        if soc is not None and tgtA is not None and preA is not None and preV is not None:
            parsed_data.append({
                'soc': soc,
                'tgtA': tgtA,
                'preA': preA,
                'preV': preV
            })

# CSV 파일로 저장
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['soc', 'tgtA', 'preA', 'preV']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(parsed_data)

print(f"Parsed data has been saved to {output_path}")