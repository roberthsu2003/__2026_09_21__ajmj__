# BMI 計算與多項選擇判斷

# 1. 取得使用者輸入的身高與體重
height_cm = float(input("請輸入您的身高 (公分): "))
weight_kg = float(input("請輸入您的體重 (公斤): "))

# 2. 將身高轉換為公尺，並計算 BMI
height_m = height_cm / 100
bmi = weight_kg / (height_m ** 2)

# 3. 使用多項選擇判斷體重狀態
if bmi < 18.5:
    status = "體重過輕"
elif bmi < 24:
    status = "健康正常範圍"
elif bmi < 27:
    status = "過重"
elif bmi < 30:
    status = "輕度肥胖"
elif bmi < 35:
    status = "中度肥胖"
else:
    status = "重度肥胖"

# 4. 輸出結果
print(f"您的 BMI 值為: {bmi:.2f}")
print(f"您的體重狀態為: {status}")