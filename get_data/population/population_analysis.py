"""
project2_pop.csv 데이터를 Pandas DataFrame으로 로드하고 분석하는 코드
"""

import pandas as pd

# CSV 파일 로드 (cp949 인코딩)
df = pd.read_csv('project2_pop.csv', encoding='cp949')

# 데이터 기본 정보
print("=" * 50)
print("데이터 기본 정보")
print("=" * 50)
print(f"총 행 수: {len(df)}")
print(f"총 열 수: {len(df.columns)}")
print(f"\n컬럼 목록:\n{df.columns.tolist()}")

# 데이터 미리보기
print("\n" + "=" * 50)
print("데이터 미리보기 (상위 5개)")
print("=" * 50)
print(df.head())

# 기본 통계
print("\n" + "=" * 50)
print("기본 통계")
print("=" * 50)
print(df.describe())

# 유용한 분석 함수들
def get_top_population_areas(n=10):
    """유동인구가 가장 많은 상위 N개 지역 반환"""
    return df.nlargest(n, '총_유동인구_수')[['행정동_코드_명', '총_유동인구_수']]

def get_population_by_dong(dong_name):
    """특정 동의 유동인구 데이터 반환"""
    return df[df['행정동_코드_명'] == dong_name]

def get_age_distribution():
    """연령대별 유동인구 합계"""
    return {
        '10대': df['연령대_10_유동인구_수'].sum(),
        '20대': df['연령대_20_유동인구_수'].sum(),
        '30대': df['연령대_30_유동인구_수'].sum()
    }

def get_weekend_avg():
    """주말(금/토/일) 평균 유동인구"""
    weekend_cols = ['금요일_유동인구_수', '토요일_유동인구_수', '일요일_유동인구_수']
    return df[weekend_cols].mean()

# 추가 분석 예시
def analyze_data():
    """종합 분석"""
    print("\n" + "=" * 50)
    print("종합 분석")
    print("=" * 50)
    
    # 1. 상위 10개 지역
    print("\n[유동인구 상위 10개 지역]")
    print(get_top_population_areas(10))
    
    # 2. 연령대별 분포
    print("\n[연령대별 유동인구 합계]")
    age_dist = get_age_distribution()
    for age, count in age_dist.items():
        print(f"{age}: {count:,}명")
    
    # 3. 주말 평균
    print("\n[요일별 평균 유동인구]")
    weekend_avg = get_weekend_avg()
    print(weekend_avg)
    
    # 4. 전체 통계
    print(f"\n[전체 유동인구 합계]")
    print(f"{df['총_유동인구_수'].sum():,}명")

if __name__ == '__main__':
    analyze_data()
