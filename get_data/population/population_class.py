"""
project2_pop.csv 데이터를 객체 지향 방식으로 다루는 코드
"""

from dataclasses import dataclass
from typing import List
import csv

@dataclass
class PopulationData:
    """유동인구 데이터 클래스"""
    기준_년분기_코드: str
    행정동_코드: str
    행정동_코드_명: str
    총_유동인구_수: int
    연령대_10_유동인구_수: int
    연령대_20_유동인구_수: int
    연령대_30_유동인구_수: int
    금요일_유동인구_수: int
    토요일_유동인구_수: int
    일요일_유동인구_수: int
    
    @property
    def weekend_average(self) -> float:
        """주말 평균 유동인구"""
        return (self.금요일_유동인구_수 + self.토요일_유동인구_수 + self.일요일_유동인구_수) / 3
    
    @property
    def youth_ratio(self) -> float:
        """10-30대 비율"""
        youth = self.연령대_10_유동인구_수 + self.연령대_20_유동인구_수 + self.연령대_30_유동인구_수
        return (youth / self.총_유동인구_수 * 100) if self.총_유동인구_수 > 0 else 0
    
    def __str__(self):
        return f"{self.행정동_코드_명}: 총 {self.총_유동인구_수:,}명"


class PopulationDatabase:
    """유동인구 데이터베이스 관리 클래스"""
    
    def __init__(self, csv_file: str):
        self.data: List[PopulationData] = []
        self.load_from_csv(csv_file)
    
    def load_from_csv(self, csv_file: str):
        """CSV 파일에서 데이터 로드"""
        with open(csv_file, 'r', encoding='cp949') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pop_data = PopulationData(
                    기준_년분기_코드=row['기준_년분기_코드'],
                    행정동_코드=row['행정동_코드'],
                    행정동_코드_명=row['행정동_코드_명'],
                    총_유동인구_수=int(row['총_유동인구_수']),
                    연령대_10_유동인구_수=int(row['연령대_10_유동인구_수']),
                    연령대_20_유동인구_수=int(row['연령대_20_유동인구_수']),
                    연령대_30_유동인구_수=int(row['연령대_30_유동인구_수']),
                    금요일_유동인구_수=int(row['금요일_유동인구_수']),
                    토요일_유동인구_수=int(row['토요일_유동인구_수']),
                    일요일_유동인구_수=int(row['일요일_유동인구_수'])
                )
                self.data.append(pop_data)
    
    def find_by_dong(self, dong_name: str) -> List[PopulationData]:
        """동 이름으로 검색"""
        return [d for d in self.data if dong_name in d.행정동_코드_명]
    
    def find_by_code(self, code: str) -> List[PopulationData]:
        """행정동 코드로 검색"""
        return [d for d in self.data if d.행정동_코드 == code]
    
    def get_top_n(self, n: int = 10) -> List[PopulationData]:
        """유동인구 상위 N개 지역"""
        return sorted(self.data, key=lambda x: x.총_유동인구_수, reverse=True)[:n]
    
    def get_total_population(self) -> int:
        """전체 유동인구 합계"""
        return sum(d.총_유동인구_수 for d in self.data)
    
    def get_age_statistics(self) -> dict:
        """연령대별 통계"""
        return {
            '10대': sum(d.연령대_10_유동인구_수 for d in self.data),
            '20대': sum(d.연령대_20_유동인구_수 for d in self.data),
            '30대': sum(d.연령대_30_유동인구_수 for d in self.data)
        }
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]


# 사용 예시
if __name__ == '__main__':
    # 데이터베이스 로드
    db = PopulationDatabase('project2_pop.csv')
    
    print(f"총 데이터 수: {len(db)}")
    print(f"전체 유동인구: {db.get_total_population():,}명")
    
    # 상위 10개 지역
    print("\n[유동인구 상위 10개 지역]")
    for i, pop in enumerate(db.get_top_n(10), 1):
        print(f"{i}. {pop}")
    
    # 연령대별 통계
    print("\n[연령대별 통계]")
    age_stats = db.get_age_statistics()
    for age, count in age_stats.items():
        print(f"{age}: {count:,}명")
    
    # 특정 동 검색
    print("\n[강남 관련 지역 검색]")
    gangnam = db.find_by_dong('강남')
    for pop in gangnam[:5]:
        print(f"  {pop.행정동_코드_명}: {pop.총_유동인구_수:,}명 (청년비율: {pop.youth_ratio:.1f}%)")
