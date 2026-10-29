"""Google Cloud Run 배포용 정렬 알고리즘 시각화 백엔드 서버 (FastAPI)

셸 정렬, 퀵 정렬, 병합 정렬의 상태 스냅샷을 수집하여
단일 타임라인 애니메이션 재생을 위한 JSON 데이터를 클라이언트에 제공합니다.
"""

import os
import random
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 스냅샷 수집 알고리즘 임포트
from algorithms import record_merge_sort, record_quick_sort, record_shell_sort

app = FastAPI(
    title="Algorithm Visualization API",
    description="셸 정렬, 퀵 정렬, 병합 정렬의 상태 스냅샷 및 비교 분석 API",
    version="1.0.0",
)

# CORS 설정: 브라우저 및 Google Apps Script(GAS)에서의 원활한 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SortRequest(BaseModel):
    """정렬 요청 데이터 모델"""
    array: Optional[List[int]] = Field(
        default=None,
        description="정렬할 정수 배열. 생략 시 size 크기만큼 랜덤 배열 자동 생성",
        examples=[[38, 27, 43, 3, 9, 82, 10]],
    )
    size: Optional[int] = Field(
        default=10,
        ge=4,
        le=30,
        description="배열 미제공 시 랜덤 생성할 원소 개수 (4 ~ 30 권장)",
    )


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/health", response_model=HealthResponse, summary="서버 헬스 체크")
def health_check() -> HealthResponse:
    """Cloud Run 컨테이너 상태 점검 및 클라이언트 연결 확인 엔드포인트"""
    return HealthResponse(
        status="ok",
        service="algorithm-visualizer-backend",
        version="1.0.0",
    )


@app.post("/api/sort", summary="3개 정렬 알고리즘 스냅샷 일괄 생성")
def generate_sort_snapshots(payload: SortRequest) -> Dict[str, Any]:
    """셸 정렬, 퀵 정렬, 병합 정렬을 끝까지 실행하고

    각 알고리즘의 동작 스냅샷 히스토리와 메타데이터를 반환합니다.
    """
    try:
        # 1. 대상 배열 결정 (사용자 제공 배열 또는 랜덤 배열)
        if payload.array is not None:
            if not isinstance(payload.array, list):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="입력 'array'는 정수 리스트 형태여야 합니다.",
                )
            if len(payload.array) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="정렬을 수행하려면 최소 2개 이상의 원소가 필요합니다.",
                )
            if len(payload.array) > 50:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="시각화 애니메이션의 원활한 표현을 위해 배열 길이는 최대 50개 이하로 제한됩니다.",
                )
            target_array = payload.array
        else:
            # 기본 랜덤 배열 생성 (10 ~ 99 범위의 고유한 난수)
            size = payload.size or 10
            target_array = random.sample(range(10, 100), size)

        # 2. 각 알고리즘별 스냅샷 히스토리 기록
        shell_result = record_shell_sort(target_array)
        quick_result = record_quick_sort(target_array)
        merge_result = record_merge_sort(target_array)

        # 3. 단일 타임라인 동기화를 위한 최대 스텝 수 계산
        max_steps = max(
            shell_result["total_steps"],
            quick_result["total_steps"],
            merge_result["total_steps"],
        )

        return {
            "status": "success",
            "message": "스냅샷 생성이 성공적으로 완료되었습니다.",
            "initial_array": target_array,
            "array_size": len(target_array),
            "max_steps": max_steps,
            "results": {
                "shell_sort": shell_result,
                "quick_sort": quick_result,
                "merge_sort": merge_result,
            },
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"알고리즘 스냅샷 생성 중 서버 오류 발생: {str(exc)}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    # Cloud Run은 환경 변수 PORT를 주입합니다. (기본값 8080)
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)

