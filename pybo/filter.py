def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)

def format_category(value):     # 카테고리 한글 변환 필터 (2022-07-01)
    return value.replace('qna', 'Q&A').replace('lesson', '강좌').replace('free', '자유게시판')
