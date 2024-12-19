import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# x와 y 값 (7개씩)
x_values = np.array([350, 360, 370, 380, 390, 400, 410])  # x 값
y_values = np.array([300, 400, 500, 600, 700, 800, 900])  # y 값

# 예시 z 값 (실제 측정 데이터)
# 이 값을 실제 측정값에 맞게 조정하세요. 예를 들어:
# z_values = np.array([9.29, 9.39, 8.53, 8.06, 8.52, 8.78, 7.03, 9.47, 9.9, 8.77, 9.21, 8.81, 9.06, 7.4, 8.84, 9.68, 8.96, 8.65, 8.94, 8.41, 8.5, 8.86, 9.6, 9.67, 8.53, 9, 8.43, 6.83, 9.09, 9.92, 9.38, 8.8, 9.26, 8.64, 7.07, 10.1, 9.49, 9.51, 8.43, 8.9, 8.31, 7.48, 10.36, 10.05, 10, 9.08, 8.66, 8.95, 7.34 ])
z_values = np.array([9.29, 9.47, 8.84, 8.86, 9.09, 10.1, 10.36, 9.39, 8.9, 9.68, 9.6, 9.92, 9.49, 10.05, 8.53, 8.77, 8.96, 9.67, 9.38, 9.51, 10, 8.06, 9.21, 8.65, 8.53, 8.8, 8.43, 9.08, 8.52, 8.81, 8.94, 9, 9.26, 8.9, 8.66, 8.78, 9.06, 8.41, 8.43, 8.64, 8.31, 8.95, 7.03, 7.4, 8.5, 6.83, 7.07, 7.48, 7.34])

# 모든 x, y 조합에 대한 z 값 계산 (49개의 값)
X = np.array([[x, y] for x in x_values for y in y_values])

# 회귀 모델 학습
model = LinearRegression()
model.fit(X, z_values)

# 회귀 모델의 계수와 절편
a1, a2 = model.coef_  # x와 y에 대한 기울기
b = model.intercept_  # 절편

print(f"모델 수식: z = {a1} * x + {a2} * y + {b}")

# 학습된 회귀 모델을 통해 z 예측
z_pred = model.predict(X)

# 예측된 z 값 출력
print("++++++++++++++++++++++++++++++")
print("학습된 회귀 모델을 이용한 z 예측 값:")
print(z_pred)

# 실제 값과 예측 값의 비교 그래프 출력
plt.figure(figsize=(10, 6))

# 실제 값 (점으로 표시)
plt.scatter(range(len(z_values)), z_values, color='blue', label='real')

# 예측 값 (선으로 표시)
plt.plot(range(len(z_pred)), z_pred, color='red', linestyle='--', label='predict')

# x 값이 바뀔 때마다 구분선과 x 값 추가
for i in range(1, len(x_values)*len(y_values)):
    if i % len(y_values) == 0:
        plt.axvline(x=i - 0.5, color='gray', linestyle=':', linewidth=1)  # 구분선
        x_label_pos = i - len(y_values) // 2  # x 값의 중간 위치에 텍스트 표시
        plt.text(x_label_pos, min(z_values) - 5, f"x = {x_values[i // len(y_values)]}", ha='center', va='center', fontsize=10, color='black')  # x 값 텍스트


# 그래프 제목과 레이블
plt.title('compare real with predict')
plt.xlabel('data index')
plt.ylabel('z value')

# 범례 추가
plt.legend()

# 그래프 표시
plt.show()


# 새로운 x, y 값에 대해 z 예측 (예시)
new_x = np.array([350, 360, 370, 380, 390, 400, 410])  # 새로운 y 값
new_y = np.array([350, 450, 550, 650, 750, 850, 950])  # 새로운 x 값

#new_x = np.array([350, 450, 550, 650, 750, 850, 950])  # 새로운 x 값
#new_y = np.array([350, 360, 370, 380, 390, 400, 410])  # 새로운 y 값

# 예측
new_X = np.column_stack((new_x, new_y))
new_z_pred = model.predict(new_X)

print("새로운 x, y 값에 대한 z 예측 결과:")
print(new_z_pred)
