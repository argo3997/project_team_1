import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API")

# @@@@@@ 파일명 입력 @@@@@@
filename = "./youtube_여의도_맛집_20260109_174932.json"

def get_video_details(video_ids, parts=["snippet", "contentDetails", "statistics"]):
    """
    YouTube 동영상 세부 정보를 가져와서 JSON 파일로 저장
    
    Args:
        video_ids (list): 비디오 ID 리스트
        parts (list): 가져올 정보 파트 (snippet, contentDetails, statistics, id 등)
    
    Returns:
        dict: 전체 응답 데이터
    """
    
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    
    all_items = []
    
    # API는 한 번에 최대 50개의 ID만 처리 가능
    batch_size = 50
    
    for i in range(0, len(video_ids), batch_size):
        batch_ids = video_ids[i:i+batch_size]
        
        params = {
            "key": API_KEY,
            "part": ",".join(parts),
            "id": ",".join(batch_ids)
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            all_items.extend(items)
            
            print(f"가져온 데이터: {len(items)}개 (총: {len(all_items)}개)")
            
        except requests.exceptions.RequestException as e:
            print(f"API 요청 실패: {e}")
            break
    
    # 최종 결과 구성
    result = {
        "kind": "youtube#videoListResponse",
        "pageInfo": {
            "totalResults": len(all_items),
            "resultsPerPage": len(all_items)
        },
        "items": all_items
    }
    
    # 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"youtube_video_details_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n파일 저장 완료: {filename}")
    print(f"총 {len(all_items)}개의 비디오 세부 정보를 저장했습니다.")
    
    return result


def extract_video_ids_from_search_result(search_json_file):
    """
    검색 결과 JSON 파일에서 video ID 추출
    
    Args:
        search_json_file (str): 검색 결과 JSON 파일 경로
    
    Returns:
        list: video ID 리스트
    """
    with open(search_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    video_ids = []
    for item in data.get("items", []):
        if "id" in item and "videoId" in item["id"]:
            video_ids.append(item["id"]["videoId"])
    
    print(f"추출된 video ID 개수: {len(video_ids)}")
    return video_ids


# 사용 예시
if __name__ == "__main__":
    # 방법 1: 저장된 검색 결과 파일에서 video ID 추출
    search_file = filename  
    video_ids = extract_video_ids_from_search_result(search_file)
    
    # 방법 2: 직접 video ID 리스트 제공
    # video_ids = ["rTtlAiAEPVI", "47YkvOc7oDg", "I_1xxB-8-eQ"]
    
    # 세부 정보 가져오기
    result = get_video_details(
        video_ids=video_ids,
        parts=["snippet", "contentDetails", "statistics", "id"]
    )