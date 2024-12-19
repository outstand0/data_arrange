import re
import csv
from collections import defaultdict
from tkinter import Tk, filedialog
import os

# 파일 선택 창 띄우기
def select_file():
    root = Tk()
    root.withdraw()  # Tkinter GUI 창 숨김
    file_path = filedialog.askopenfilename(title="Select Log File", filetypes=[("Log files", "*.log")])
    return file_path

# 결과 파일 경로 생성 함수
def generate_output_path(file_path):
    file_dir, file_name = os.path.split(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    return os.path.join(file_dir, f"{file_name_without_ext}_parsed.csv")

# 파일 경로 설정
file_path = select_file()
if not file_path:
    print("No file selected. Exiting...")
    exit()

output_path = generate_output_path(file_path)

# 결과 저장을 위한 리스트 초기화
parsed_data = []
soc_ranges = defaultdict(list)

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
        # 다음 줄에서 `preA`, `preV`, `maxA` 추출
        preA_match = re.search(r"preA\((\d+),", next_line)
        preV_match = re.search(r"preV\((\d+),", next_line)
        maxA_match = re.search(r"maxA\((\d+),", next_line)

        preA = float(preA_match.group(1)) / 10 if preA_match else None
        preV = int(preV_match.group(1)) / 10 if preV_match else None
        maxA = float(maxA_match.group(1)) if maxA_match else None

        # `soc`, `tgtA`, `preA`, `preV`, `maxA`가 모두 존재할 때 데이터 추가
        if soc is not None and tgtA is not None and preA is not None and preV is not None and maxA is not None:
            avg_pwr = round(preA * preV, 2)  # preA * preV 계산

            parsed_data.append({
                'soc': soc,
                'tgtA': tgtA,
                'preA': preA,
                'preV': preV,
                'maxA': maxA
            })

            # soc 값을 10% 구간으로 나누기
            soc_range = soc // 10 * 10  # soc 값을 10의 배수로 구간화 (예: 23 -> 20)
            soc_ranges[soc_range].append({
                'tgtA': tgtA,
                'preA': preA,
                'preV': preV,
                'maxA': maxA,
                'avg_pwr': avg_pwr
            })

# 평균 계산
average_data = []
for soc_range, values in soc_ranges.items():
    avg_tgtA = sum(v['tgtA'] for v in values) / len(values)
    avg_preA = sum(v['preA'] for v in values) / len(values)
    avg_preV = sum(v['preV'] for v in values) / len(values)
    avg_maxA = sum(v['maxA'] for v in values) / len(values)    
    avg_pwr = avg_preA * avg_preV / 1000

    average_data.append({
        'soc_range': f"{soc_range}~{soc_range + 9}%",
        'avg_tgtA': round(avg_tgtA, 2),
        'avg_preA': round(avg_preA, 2),
        'avg_preV': round(avg_preV, 2),
        'avg_maxA': round(avg_maxA, 2),
        'avg_pwr': round(avg_pwr, 2)
    })

# CSV 파일로 저장 (평균값을 상단에, 원본 데이터는 그 다음에 저장)
fieldnames = ['soc_range', 'avg_maxA', 'avg_tgtA', 'avg_preA', 'avg_preV', 'avg_pwr', 'soc', 'maxA', 'tgtA', 'preA', 'preV']

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 헤더 작성
    for avg in average_data:
        writer.writerow(avg)  # 평균값 작성
    for row in parsed_data:
        writer.writerow(row)  # 원본 데이터 작성

print(f"Parsed data with averages has been saved to {output_path}")
