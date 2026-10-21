from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Insertion Sort API")

# GAS 및 웹 앱과의 Cross-Origin 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SortRequest(BaseModel):
    numbers: List[int]

@app.get("/")
def read_root():
    """서버 헬스체크용 엔드포인트"""
    return {"status": "ok", "message": "Insertion Sort API Server is running"}

@app.post("/sort")
def insertion_sort(req: SortRequest) -> Dict[str, Any]:
    """
    단순 삽입 정렬 알고리즘 수행 및 단계별 상태 기록
    
    [시간 복잡도]
    - 최악/평균: O(n^2)
    - 최선: O(n) (이미 정렬되어 있는 경우)
    
    [공간 복잡도]
    - O(1) (제자리 정렬)
    """
    arr = list(req.numbers)
    steps = []
    
    # 초깃값 기록 (0단계)
    steps.append({
        "step": 0,
        "array": list(arr),
        "target_index": -1,
        "compare_index": -1,
        "description": "정렬 시작 전 초기 배열 상태입니다."
    })
    
    step_count = 1
    n = len(arr)
    
    # 1번째 인덱스부터 마지막 인덱스까지 순회 (삽입할 대상 지정)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        # 현재 선택된 key 값을 앞쪽 정렬된 서브 배열과 비교하며 자리 찾기
        while j >= 0 and arr[j] > key:
            steps.append({
                "step": step_count,
                "array": list(arr),
                "target_index": i,
                "compare_index": j,
                "description": f"인덱스 {j}의 값 ({arr[j]})이 삽입할 값 ({key})보다 크므로 오른쪽(인덱스 {j+1})으로 이동시킵니다."
            })
            step_count += 1
            
            arr[j + 1] = arr[j]
            j -= 1
            
        arr[j + 1] = key
        
        steps.append({
            "step": step_count,
            "array": list(arr),
            "target_index": j + 1,
            "compare_index": -1,
            "description": f"삽입할 값 ({key})을 올바른 위치인 인덱스 {j+1}에 안착시켰습니다."
        })
        step_count += 1

    return {
        "original": req.numbers,
        "sorted": arr,
        "steps": steps,
        "total_steps": len(steps) - 1,
        "complexity": {
            "time_best": "O(n)",
            "time_average": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)"
        }
    }
