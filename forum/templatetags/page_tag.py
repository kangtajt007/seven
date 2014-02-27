#coding:utf-8

from django import template

register = template.Library()

def percent_decimal(value):
    value = float(str(value))
    value = round(value, 3)
    value = value * 100
    return str(value) + '%'

register.filter('percent_decimal', percent_decimal)

class Pagination(template.Node):
    def __init__(self,sequence,page_size):
        self.sequence = sequence
        self.page_size = page_size
        pass

    def render(self, context):
        page = self.sequence.resolve(context, True)
        index = page['index']
        count = page['count']
        index = int(index)
        count = int(count)
        rang = 8
        page_size = self.page_size

        if count == 0 or count <= page_size:
            return ''
        else:
            html = '<div class="pagination pagination-right"><ul>'
            page_count = count/page_size
            result = 0 if count % page_size == 0 else 1
            page_count = page_count + result
            min = 1
            max = page_count
            if index == 1:
                html += '<li class="disabled"><a href="#">&laquo;</a></li>'
            else:
                html += '<li><a href="../1">&laquo;</a></li>'

            if page_count > rang:
                a = 1
                if index <= rang/2:
                    min = 1
                    max = min + rang
                else:
                    if index >= page_count - rang/2:
                        max = page_count
                        min = max - rang
                    else:
                        while a + rang/2 != index:
                            a = a + 1
                        min = a
                        max = min + rang

                if min > 1:
                     html += '<li><a href="../'+str(min)+'">...</a></li>'

            for i in range(min, max + 1):
                if i == index:
                    html += '<li class="active">'
                else:
                    html += '<li>'
                html += '<a href="../'+str(i)+'">'+str(i)+'</a></li>'

            if page_count > rang and max < page_count:
                html += '<li><a href="../'+str(max)+'">...</a></li>'

            if index == page_count:
                html += '<li class="disabled"><a href="#">&raquo;</a></li>'
            else:
                html += '<li><a href="../'+str(page_count)+'">&raquo;</a></li>'

            return html + '</ul></div>'

def paging(parser,token):
    try:
        split = token.split_contents()
        tag_name = split[0]
        page = None
        page_size = 10
        if len(split)==2:
            page = split[1]
        elif len(split)==3:
            page = split[1]
            page_size = split[2]
    except:
        raise template.TemplateSyntaxError,"标签语法错误，后面参数为两位，分别为当前分页对象和每页记录数"

    try:
        page_size = int(page_size)
    except:
        #默认每页10条记录
        page_size = 10

    sequence = parser.compile_filter(page)
    return Pagination(sequence,page_size)

register.tag('paging', paging)