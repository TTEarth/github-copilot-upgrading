#!/usr/bin/env python3
"""
이 스크립트는 Python 2에서 Python 3으로 포팅할 때 발생하는 주요 문제들을 테스트합니다.
"""

import sys
import os

def test_cmp_function_issue():
    """cmp() 함수가 Python 3에서 제거되었음을 보여주는 테스트"""
    print("=== cmp() 함수 문제 테스트 ===")
    
    try:
        # Python 2에서는 가능했지만 Python 3에서는 오류
        result = cmp(5, 3)  # NameError 발생
        print(f"cmp(5, 3) = {result}")
    except NameError as e:
        print(f"❌ 오류: {e}")
        print("💡 해결책: (a > b) - (a < b) 또는 functools.cmp_to_key() 사용")
        
        # 해결책 1: 직접 구현
        def cmp_replacement(a, b):
            return (a > b) - (a < b)
        
        result = cmp_replacement(5, 3)
        print(f"✅ cmp_replacement(5, 3) = {result}")

        # 해결책 2: functools.cmp_to_key 사용 (정렬에 사용할 때)
        from functools import cmp_to_key
        
        class Item:
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return f"Item({self.name})"
        
        items = [Item("c"), Item("a"), Item("b")]
        
        def compare_items(item1, item2):
            return cmp_replacement(item1.name, item2.name)
        
        sorted_items = sorted(items, key=cmp_to_key(compare_items))
        print(f"✅ 정렬된 항목들: {sorted_items}")

def test_exception_syntax():
    """Python 2 스타일 예외 처리 구문 문제를 보여주는 테스트"""
    print("\n=== Exception 구문 문제 테스트 ===")
    
    # Python 2 스타일 (구문 오류)
    test_code_py2 = """
try:
    raise ValueError("test error")
except ValueError, e:  # Python 2 스타일
    print("Caught:", str(e))
"""
    
    print("❌ Python 2 스타일 예외 처리:")
    print(test_code_py2.strip())
    print("위 코드는 Python 3에서 SyntaxError를 발생시킵니다.")
    
    # Python 3 호환 스타일
    print("\n✅ Python 3 호환 예외 처리:")
    try:
        raise ValueError("test error")
    except ValueError as e:  # Python 3 스타일 (Python 2.6+에서도 동작)
        print(f"정상적으로 예외 처리됨: {e}")

def test_unicode_literals():
    """Unicode 리터럴 처리 차이를 보여주는 테스트"""
    print("\n=== Unicode 리터럴 문제 테스트 ===")
    
    # Python 2에서는 u'' 필요했지만 Python 3에서는 불필요
    unicode_string = "한글 텍스트"  # Python 3에서는 기본적으로 unicode
    
    print(f"✅ Python 3에서 문자열: {unicode_string}")
    print(f"✅ 문자열 타입: {type(unicode_string)}")
    
    # Python 2에서 u'ok' 였던 것이 Python 3에서는 'ok'로 충분
    integrity_check = ('ok',)  # u'ok' 불필요
    print(f"✅ 무결성 체크 튜플: {integrity_check}")

def test_file_handling():
    """파일 처리 방식 개선을 보여주는 테스트"""
    print("\n=== 파일 처리 개선 테스트 ===")
    
    test_file = "/tmp/test_python_port.txt"
    test_content = "테스트 내용입니다."
    
    # 구식 방법 (Python 2 스타일)
    print("❌ 구식 파일 처리 방법:")
    print("""
f = open('file.txt', 'w')
try:
    f.write(content)
finally:
    f.close()  # 명시적으로 닫아야 함
""")
    
    # 현대적 방법 (Python 3 권장)
    print("✅ 현대적 파일 처리 방법 (context manager):")
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"파일에 내용 작성 완료: {test_file}")
        
        with open(test_file, 'r', encoding='utf-8') as f:
            read_content = f.read()
        print(f"파일에서 읽은 내용: {read_content}")
        
        # 정리
        os.remove(test_file)
        print("테스트 파일 삭제 완료")
        
    except Exception as e:
        print(f"파일 처리 중 오류: {e}")

def test_print_function():
    """print 문에서 함수로의 변경을 보여주는 테스트"""
    print("\n=== print 문/함수 문제 테스트 ===")
    
    print("❌ Python 2 스타일:")
    print("print 'Hello, World!'  # 구문")
    
    print("\n✅ Python 3 스타일:")
    print("print('Hello, World!')  # 함수")
    print("현재 이 코드는 이미 Python 3 스타일입니다!")

def main():
    """메인 테스트 실행"""
    print(f"Python 버전: {sys.version}")
    print(f"Python 메이저 버전: {sys.version_info.major}")
    print("=" * 50)
    
    if sys.version_info.major < 3:
        print("❌ 이 스크립트는 Python 3에서 실행되어야 합니다.")
        return
    
    test_cmp_function_issue()
    test_exception_syntax()
    test_unicode_literals()
    test_file_handling()
    test_print_function()
    
    print("\n" + "=" * 50)
    print("🎉 모든 테스트가 완료되었습니다!")
    print("💡 이 결과들은 Python 2에서 Python 3으로 포팅할 때")
    print("   주의해야 할 주요 사항들을 보여줍니다.")

if __name__ == "__main__":
    main()