"""퀵 정렬 (Quick Sort) 알고리즘 구현

- 분할 정복(Divide and Conquer) 기법 사용
- 평균 시간 복잡도: O(N log N)
- 최악 시간 복잡도: O(N^2)
"""

from typing import List


def quick_sort_pythonic(arr: List[int]) -> List[int]:
    """간결하고 직관적인 퀵 정렬 (추가 메모리 사용)"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort_pythonic(left) + middle + quick_sort_pythonic(right)


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """메모리를 절약하는 제자리(In-place) 퀵 정렬 (Lomuto 분할 방식)"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = _partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


if __name__ == "__main__":
    test_data = [38, 27, 43, 3, 9, 82, 10]
    print(f"원본 데이터: {test_data}")

    # 1. 직관적 방식 테스트
    sorted_pythonic = quick_sort_pythonic(test_data)
    print(f"Pythonic 정렬 결과: {sorted_pythonic}")

    # 2. In-place 방식 테스트
    data_copy = test_data.copy()
    quick_sort_inplace(data_copy)
    print(f"In-place 정렬 결과: {data_copy}")

    assert sorted_pythonic == sorted(test_data)
    assert data_copy == sorted(test_data)
    print("모든 정렬 테스트 통과!")

