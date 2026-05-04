import pandas as pd
import numpy as np

def calculate_total_resistance(particle_size, pb_thickness=3, ref_size=150):
    """
    입자 크기와 PB 증착 두께에 따른 총 상대 저항 계산
    """
    # 1. 소결체 단독 상대 저항 (R_s)
    # 입자 크기에 반비례하는 특성 (D^-1)
    base_resistance = ref_size / particle_size
    
    # 2. PB 증착에 의한 추가 저항 (R_pb)
    # 입자 크기가 작을수록 비표면적이 넓어져 PB 코팅의 영향이 커짐
    # PB는 반도체적 특성이므로 금속 대비 저항 가중치 부여
    surface_area_factor = (ref_size / particle_size) ** 2
    pb_effect = 0.5 * (pb_thickness / 3) * surface_area_factor if pb_thickness > 0 else 0
    
    total_r = base_resistance + pb_effect
    return round(total_r, 2)

# 데이터 생성: 중간 입자 유형 (30~150μm)
sizes = np.arange(30, 151, 5)[::-1] # 150부터 30까지 역순
data = []

for d in sizes:
    r_total = calculate_total_resistance(d, pb_thickness=3 if d <= 45 else 0)
    
    # 역할 정의
    if d >= 140:
        role = "Flash (초기 흡수)"
    elif d >= 80:
        role = "Bridge (전하 전이)"
    else:
        role = "Concentration (최종 농축)"
        
    data.append([f"{d}μm", r_total, role])

# 결과 출력
df = pd.DataFrame(data, columns=['입자 크기', '상대 총 저항 (R_total)', '설계상 역할'])
print("### 입자별 저항 구배 시뮬레이션 결과 ###")
print(df.to_markdown(index=False))

# 특정 구간 (45μm PB 포함) 상세 분석
r_45_pure = calculate_total_resistance(45, pb_thickness=0)
r_45_pb = calculate_total_resistance(45, pb_thickness=3)
print(f"\n[분석] 45μm 단독 저항: {r_45_pure} / PB 3μm 증착 후: {r_45_pb} (약 {round(r_45_pb/r_45_pure, 1)}배 증가)")