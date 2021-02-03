# -*- coding:utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import re

class trim:

    def init(self):
        print("Init trim class...")

    def pure_url(self, target_text):
        #### Goal ====================================================================
        # target : /url?q=http://www.akomnews.com/bbs/board.php%3Fbo_table%3Dnews%26wr_id%3D42804&amp;sa=U&amp;ved=2ahUKEwjUu7iQrfXtAhVbQd4KHQqjDsAQxfQBMAB6BAgBEAE&amp;usg=AOvVaw1wbQMVtf-ZFmSIHmURqsbf
        # result : http://www.akomnews.com/bbs/board.php?bo_table=news&wr_id=42804
        
        replace_text = [
            ['/url?q=', ''],
            ['%3F', '?'],
            ['%3D', '='],
            ['%26', '&']
        ]
        re_p = re.compile(r'&sa.*', re.I)

        for r in replace_text:
            target_text = target_text.replace(r[0], r[1])

        result_text = re_p.sub('', target_text)
        return result_text
    
    def pure_daum_news_provider(self, original):
        # target :  2020.11.16 | 12시간전 | OO일보 | 다음뉴스 
        reg_list = [
            re.compile(r'^\s\d{1,2}시간전\s\|\s'),
            re.compile(r'^\s\d{1,2}분전\s\|\s'),
            re.compile(r'\s\|\s다음뉴스\s'),
            re.compile(r'\d{1,4}\.\d{1,2}\.\d{1,2}\s\|')]

        for reg in reg_list:
            original = reg.sub('', original)
        
        return original

    def pure_naver_news_provider(self, original):
        reg_list = [
            re.compile(r'언론사 선정')]

        for reg in reg_list:
            original = reg.sub('', original)
        
        return original


if __name__ == '__main__':
    test_text = '/url?q=http://www.akomnews.com/bbs/board.php%3Fbo_table%3Dnews%26wr_id%3D42804&sa=U&amp;ved=2ahUKEwjUu7iQrfXtAhVbQd4KHQqjDsAQxfQBMAB6BAgBEAE&amp;usg=AOvVaw1wbQMVtf-ZFmSIHmURqsbf'
    # Expect Result : http://www.akomnews.com/bbs/board.php?bo_table=news&wr_id=42804

    trim = trim()
    result_text = trim.pure_url(test_text)

    print("[ Test Complete : pure_url ]" + "=" * 50)
    print(result_text)