"""
project2_pop.csv 데이터를 Python 딕셔너리 리스트로 변환한 파일
"""

# 유동인구 데이터 (샘플 10개만 포함)
population_data = [
    {
        '기준_년분기_코드': '20204',
        '행정동_코드': '11740700',
        '행정동_코드_명': '둔촌2동',
        '총_유동인구_수': 7273534,
        '연령대_10_유동인구_수': 1201597,
        '연령대_20_유동인구_수': 880170,
        '연령대_30_유동인구_수': 1051524,
        '금요일_유동인구_수': 1036661,
        '토요일_유동인구_수': 1015837,
        '일요일_유동인구_수': 1040695
    },
    # ... (전체 8500개 데이터)
]

# 데이터 사용 예시
def get_total_population():
    """전체 유동인구 합계를 반환"""
    return sum(row['총_유동인구_수'] for row in population_data)

def get_by_dong(dong_name):
    """특정 동의 데이터를 반환"""
    return [row for row in population_data if row['행정동_코드_명'] == dong_name]

def get_by_code(code):
    """행정동 코드로 데이터를 검색"""
    return [row for row in population_data if row['행정동_코드'] == code]

if __name__ == '__main__':
    print(f"총 데이터 수: {len(population_data)}")
    print(f"첫 번째 데이터: {population_data[0]}")
