# Python 2 to 3 포팅 시 발생 가능한 문제점 분석

이 문서는 이 레거시 Python 2.5 프로젝트를 최신 Python 3으로 포팅할 때 발생할 수 있는 주요 문제점들을 분석합니다.

## 🔍 발견된 주요 문제점들

### 1. **`cmp()` 함수 제거** - 🚨 Critical
**위치**: `distribute_setup.py:449`
```python
def sorter(dir1, dir2):
    return cmp(dir1.name, dir2.name)  # ❌ Python 3에서 제거됨
```

**문제**: Python 3에서 내장 `cmp()` 함수가 완전히 제거되었습니다.

**해결방안**:
```python
def sorter(dir1, dir2):
    # Python 3 compatible approach
    return (dir1.name > dir2.name) - (dir1.name < dir2.name)
```

또는 더 나은 방법으로 `functools.cmp_to_key()` 사용:
```python
from functools import cmp_to_key
directories.sort(key=cmp_to_key(sorter))
```

### 2. **Exception 처리 구문 변경** - 🔶 Medium
**위치**: 여러 파일에서 예상됨
```python
except Exception, e:  # ❌ Python 2 스타일
```

**문제**: Python 2의 `except Exception, e:` 구문이 Python 3에서 구문 오류가 됩니다.

**해결방안**:
```python
except Exception as e:  # ✅ Python 2.6+ 및 Python 3 호환
```

### 3. **파일 처리 및 Context Manager** - 🔶 Medium
**위치**: `distribute_setup.py:209, 216, 225`
```python
existing_content = open(path).read()  # ❌ 파일이 자동으로 닫히지 않음
f = open(path, 'w')
try:
    f.write(content)
finally:
    f.close()  # ❌ 비효율적
```

**문제**: 적절한 파일 핸들링이 없고 context manager를 사용하지 않습니다.

**해결방안**:
```python
with open(path, 'r') as f:
    existing_content = f.read()

with open(path, 'w') as f:
    f.write(content)
```

### 4. **Unicode/String 처리 변경** - 🔶 Medium
**위치**: `database.py:41, 83`
```python
return row[0]  # Python 2: str/unicode 구분
if integrity == (u'ok',):  # ❌ u'' 리터럴 불필요
```

**문제**: Python 2의 unicode 리터럴 `u''`와 string/unicode 구분이 Python 3에서 달라집니다.

**해결방안**:
```python
if integrity == ('ok',):  # ✅ Python 3에서는 u'' 불필요
```

### 5. **SQLite 예외 처리 변경** - 🔷 Low (이미 부분적으로 해결됨)
**위치**: 테스트에서 발견됨
```python
self.assertRaises(sqlite3.InterfaceError, foo.__setitem__, 'bar', {'a':'b'})
```

**문제**: Python 3.12에서 SQLite 오류 타입이 `InterfaceError`에서 `ProgrammingError`로 변경되었습니다.

### 6. **Import 모듈 경로 변경** - 🔷 Low (이미 해결됨)
**위치**: `config.py:1`
```python
from configparser import ConfigParser  # ✅ 이미 올바름
```

**확인된 사항**: `ConfigParser` 모듈은 이미 올바르게 Python 3 스타일로 import되고 있습니다.

### 7. **print 문에서 함수로 변경** - 🔷 Low
**검사 결과**: 코드에서 `print` 문은 발견되지 않았습니다.

### 8. **setup.py의 호환성 선언** - 🔷 Low
**위치**: `setup.py:102-104`
```python
'Programming Language :: Python :: 2.5',  # ❌ 구버전 선언
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
```

**문제**: Python 2.5-2.7만 지원한다고 선언되어 있습니다.

**해결방안**:
```python
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.8',
'Programming Language :: Python :: 3.9',
'Programming Language :: Python :: 3.10',
'Programming Language :: Python :: 3.11',
'Programming Language :: Python :: 3.12',
```

### 9. **distribute/setuptools 의존성** - 🔶 Medium
**위치**: `setup.py:1-2`
```python
import distribute_setup
distribute_setup.use_setuptools()
```

**문제**: `distribute`는 더 이상 사용되지 않으며 `setuptools`에 통합되었습니다.

**해결방안**: 현대적인 `pyproject.toml` 사용 권장:
```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

## 🎯 우선순위별 수정 권장사항

### 🚨 Critical (즉시 수정 필요)
1. `cmp()` 함수 사용 제거 및 대체

### 🔶 Medium (조기 수정 권장)
2. Exception 처리 구문 현대화
3. 파일 처리에 context manager 사용
4. Unicode 리터럴 정리
5. 현대적인 패키징 도구로 전환

### 🔷 Low (점진적 개선)
6. setup.py의 Python 버전 호환성 선언 업데이트
7. SQLite 예외 처리 유형 업데이트

## 🧪 테스트 전략

1. **단위 테스트 실행**: 모든 기존 테스트가 통과하는지 확인
2. **통합 테스트**: 실제 사용 사례에서 동작 확인
3. **Python 버전별 테스트**: 3.8, 3.9, 3.10, 3.11, 3.12에서 테스트
4. **성능 테스트**: Python 3 포팅 후 성능 저하 없는지 확인

## 🔧 권장 도구

- **2to3**: 자동 변환 도구 (참고용)
- **pylint**: 코드 품질 검사
- **black**: 코드 포매팅 표준화
- **mypy**: 타입 힌트 및 정적 분석
- **tox**: 다중 Python 버전 테스트

## 📝 결론

이 프로젝트는 Python 2.5에서 시작된 레거시 코드로, Python 3으로 포팅하기 위해서는 주로 다음과 같은 작업이 필요합니다:

1. **Critical**: `cmp()` 함수 제거 대응
2. **Important**: 예외 처리 및 파일 처리 현대화
3. **Recommended**: 패키징 시스템 현대화

대부분의 문제는 비교적 간단한 구문 변경으로 해결 가능하며, 기존 테스트 스위트가 잘 구축되어 있어 변경 사항을 안전하게 검증할 수 있습니다.