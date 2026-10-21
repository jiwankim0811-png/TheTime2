from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(
    title="Selection Sort API",
    description="단순 선택 정렬 수행 및 단계별 정렬 상태 반환 API",
    version="1.0.0"
)

# 구글 앱스 스크립트(GAS) 및 웹 클라이언트 접속을 허용하기 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 입력 데이터 검증을 위한 Pydantic 모델
class SortRequest(BaseModel):
    numbers: List[int]

def selection_sort_with_steps(arr: List[int]) -> List[Dict[str, Any]]:
    """
    단순 선택 정렬(Selection Sort) 알고리즘을 수행하며
    각 단계(Step)의 상세 수행 상태를 기록하는 함수.
    
    시간 복잡도: O(N^2) (최선, 평균, 최악 모두 동일)
    공간 복잡도: O(1) (제자리 정렬)
    """
    steps = []
    data = arr.copy()
    n = len(data)
    step_counter = 0

    # 초기 상태 기록
    steps.append({
        "step": step_counter,
        "array": data.copy(),
        "min_idx": -1,
        "compare_idx": -1,
        "sorted_boundary": -1,
        "description": "정렬 시작 전 초기 배열 상태입니다."
    })

    # 선택 정렬 루프 수행
    for i in range(n - 1):
        min_idx = i  # 현재 정렬되지 않은 구간의 첫 번째 요소를 최솟값 위치로 임시 지정
        
        # 최솟값을 찾기 위해 나머지 요소들을 순회
        for j in range(i + 1, n):
            step_counter += 1
            steps.append({
                "step": step_counter,
                "array": data.copy(),
                "min_idx": min_idx,
                "compare_idx": j,
                "sorted_boundary": i - 1,
                "description": f"인덱스 {min_idx} (값: {data[min_idx]})와 인덱스 {j} (값: {data[j]}) 비교 중"
            })

            # 더 작은 값을 찾으면 최솟값 인덱스 갱신
            if data[j] < data[min_idx]:
                min_idx = j
                step_counter += 1
                steps.append({
                    "step": step_counter,
                    "array": data.copy(),
                    "min_idx": min_idx,
                    "compare_idx": j,
                    "sorted_boundary": i - 1,
                    "description": f"새로운 최솟값 발견! 인덱스 {min_idx} (값: {data[min_idx]})"
                })

        # 최솟값과 현재 정렬되지 않은 첫 번째 요소(i)를 교환(Swap)
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            step_counter += 1
            steps.append({
                "step": step_counter,
                "array": data.copy(),
                "min_idx": min_idx,
                "compare_idx": -1,
                "sorted_boundary": i,
                "description": f"인덱스 {i}와 인덱스 {min_idx}의 값 교환 (값: {data[i]} <-> {data[min_idx]})"
            })
        else:
            step_counter += 1
            steps.append({
                "step": step_counter,
                "array": data.copy(),
                "min_idx": min_idx,
                "compare_idx": -1,
                "sorted_boundary": i,
                "description": f"인덱스 {i}가 이미 최소값이므로 제자리 유지"
            })

    # 최종 정렬 완료 상태 추가
    step_counter += 1
    steps.append({
        "step": step_counter,
        "array": data.copy(),
        "min_idx": -1,
        "compare_idx": -1,
        "sorted_boundary": n - 1,
        "description": "선택 정렬이 최종 완료되었습니다!"
    })

    return steps

@app.get("/")
def read_root():
    """서버 헬스체크용 엔드포인트"""
    return {"status": "ok", "message": "Selection Sort Cloud Run API Running"}

@app.post("/sort/selection")
def run_selection_sort(payload: SortRequest):
    """
    선택 정렬 실행 엔드포인트
    Request Body: {"numbers": [64, 25, 12, 22, 11]}
    """
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="숫자 리스트가 비어 있습니다.")
    
    if len(payload.numbers) > 30:
        raise HTTPException(status_code=400, detail="원활한 시각화를 위해 최대 30개 이하의 숫자를 입력해주세요.")

    steps = selection_sort_with_steps(payload.numbers)

    return {
        "algorithm": "Selection Sort (단순 선택 정렬)",
        "original": payload.numbers,
        "sorted": steps[-1]["array"],
        "total_steps": len(steps),
        "steps": steps,
        "complexity": {
            "time_best": "O(N^2)",
            "time_average": "O(N^2)",
            "time_worst": "O(N^2)",
            "space": "O(1)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Cloud Run 기본 포트인 8080에 바인딩
    uvicorn.run(app, host="0.0.0.0", port=8080)
