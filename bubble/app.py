from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Bubble Sort Visualization API",
    description="Google Cloud Run 백엔드 서버: 버블 정렬 단계별 시각화 및 복잡도 제공",
    version="1.0.0"
)

# CORS 설정 (구글 앱스 스크립트 및 웹 클라이언트의 요청 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SortRequest(BaseModel):
    data: List[int]

class SortResponse(BaseModel):
    steps: List[List[int]]
    comparisons: int
    swaps: int
    time_complexity: str
    space_complexity: str
    mascot_message: str

@app.post("/bubble-sort", response_model=SortResponse)
async def bubble_sort(request: SortRequest):
    """
    버블 정렬을 수행하고 각 단계별 배열 상태와 복잡도 정보를 반환합니다.
    """
    arr = request.data.copy()
    n = len(arr)
    steps = [arr.copy()] # 초기 상태 기록
    comparisons = 0
    swaps = 0

    # 버블 정렬 알고리즘 수행
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            # 인접한 두 원소를 비교하여 앞의 원소가 더 크면 교환
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                swaps += 1
                # 상태가 변경될 때마다 단계 저장
                steps.append(arr.copy())
        
        # 최적화: 만약 이번 회차에 교환이 하나도 없었다면 이미 정렬 완료
        if not swapped:
            break

    return {
        "steps": steps,
        "comparisons": comparisons,
        "swaps": swaps,
        "time_complexity": "O(n²) [최선 O(n)]",
        "space_complexity": "O(1) (제자리 정렬)",
        "mascot_message": "안녕! 나는 버블이(Bubble-bot)야! 인접한 두 원소를 비교하며 거품처럼 큰 값을 맨 위로 밀어 올리는 버블 정렬을 함께 살펴볼까?"
    }

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Bubble Sort Cloud Run API"}
