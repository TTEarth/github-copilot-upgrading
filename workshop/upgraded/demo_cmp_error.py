#!/usr/bin/env python3
"""
distribute_setup.py의 cmp() 함수 사용으로 인한 실제 오류를 시연하는 스크립트
"""

import sys

def demonstrate_cmp_error():
    """실제 distribute_setup.py에서 발생하는 cmp() 오류 시연"""
    print("=== distribute_setup.py cmp() 오류 시연 ===")
    print(f"Python 버전: {sys.version}")
    print()
    
    # 실제 distribute_setup.py 코드 시뮬레이션
    print("distribute_setup.py:447-449 코드 시뮬레이션:")
    print("if sys.version_info < (2, 4):")
    print("    def sorter(dir1, dir2):")
    print("        return cmp(dir1.name, dir2.name)  # ← 여기서 오류!")
    print()
    
    # Python 2.4 미만인 척 하면서 cmp() 사용 시도
    class MockTarInfo:
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return f"TarInfo({self.name})"
    
    directories = [MockTarInfo("dir3"), MockTarInfo("dir1"), MockTarInfo("dir2")]
    
    print("현재 directories:", [str(d) for d in directories])
    
    # Python 2.4 미만인 경우의 코드 실행 시도
    try:
        print("\n❌ Python 2.4 미만 버전용 코드 실행 시도...")
        def sorter(dir1, dir2):
            return cmp(dir1.name, dir2.name)  # 여기서 NameError 발생!
        
        # Python 2에서는 sort(cmp_function) 가능했지만 Python 3에서는 불가능
        directories.sort(sorter)
        directories.reverse()
        print("정렬 완료:", [str(d) for d in directories])
        
    except (NameError, TypeError) as e:
        print(f"💥 오류 발생: {e}")
        if isinstance(e, NameError):
            print("🔍 원인 1: Python 3에서 cmp() 함수가 제거됨")
        elif isinstance(e, TypeError):
            print("🔍 원인 2: Python 3에서 sort()는 비교 함수를 직접 받지 않음")
        
        print("\n✅ 해결책 1: cmp() 함수 대체 구현")
        def cmp_replacement(a, b):
            return (a > b) - (a < b)
        
        def sorter_fixed(dir1, dir2):
            return cmp_replacement(dir1.name, dir2.name)
        
        # 새로운 리스트로 테스트 (원본 보존)
        test_dirs = [MockTarInfo("dir3"), MockTarInfo("dir1"), MockTarInfo("dir2")]
        
        # functools.cmp_to_key를 사용한 해결책
        from functools import cmp_to_key
        test_dirs.sort(key=cmp_to_key(sorter_fixed))
        test_dirs.reverse()
        print("해결책 1 결과:", [str(d) for d in test_dirs])
        
        print("\n✅ 해결책 2: 현대적인 Python 3 방식 (이미 구현됨)")
        import operator
        test_dirs2 = [MockTarInfo("dir3"), MockTarInfo("dir1"), MockTarInfo("dir2")]
        test_dirs2.sort(key=operator.attrgetter('name'), reverse=True)
        print("해결책 2 결과:", [str(d) for d in test_dirs2])
        
    print("\n" + "="*50)
    print("💡 결론:")
    print("- distribute_setup.py의 cmp() 사용은 Python 3에서 오류를 발생시킴")
    print("- Python 3에서 sort()도 비교 함수를 직접 받지 않음 (key= 사용 필요)")
    print("- 다행히 Python 2.4+ 버전용 코드(operator.attrgetter)가 이미 있음")
    print("- sys.version_info < (2, 4) 조건은 현재 환경에서 False이므로 실행되지 않음")
    print("- 하지만 코드 정리를 위해 cmp() 부분을 제거하는 것이 좋음")

if __name__ == "__main__":
    demonstrate_cmp_error()