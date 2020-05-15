from django.shortcuts import render
from apps.front.models import Document
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pure_pagination import PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.utils.pyecharts_restful import JsonResponse
import db_tools.data.show_data as s_data

import json
from rest_framework.views import APIView
from pyecharts.charts import Bar, Line, Pie, WordCloud, Graph
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode


# Create your views here.

def index(request):
    return render(request, 'front/index.html')


def search(request):
    search_cat_id = request.GET.get('searchtype')
    words = request.GET.get('words')

    if search_cat_id == 'title':
        if words:
            documents = Document.objects.filter(title__contains=words).all()
        else:
            documents = Document.objects.all()[:20]
    elif search_cat_id == 'author':
        if words:
            documents = Document.objects.filter(author__contains=words).all()
        else:
            documents = Document.objects.all()[:20]
    elif search_cat_id == 'source':
        if words:
            documents = Document.objects.filter(acticle_source__contains=words).all()
        else:
            documents = Document.objects.all()[:20]
    elif search_cat_id == 'keywords':
        if words:
            documents = Document.objects.filter(key_words__contains=words).all()
        else:
            documents = Document.objects.all()[:20]
    elif search_cat_id == 'summary':
        if words:
            documents = Document.objects.filter(summary__contains=words).all()
        else:
            documents = Document.objects.all()[:20]
    else:
        documents = Document.objects.all()[:20]
    context = {
        'documents': documents,
    }
    return render(request, 'front/search.html', context=context)


def document_list(request):
    all_documents = Document.objects.all()
    page = request.GET.get('page', 1)

    p = Paginator(all_documents, 20, request=request)
    documents = p.page(page)
    context = {
        'documents': documents,

    }
    return render(request, 'front/list.html', context=context)


def author_bar() -> Bar:
    x = list(s_data.authors.values())
    y = list(s_data.author_nums.values())
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("作者", y)
            .set_global_opts(title_opts=opts.TitleOpts(title="作者数量", subtitle="相关文章数量"))
            .dump_options_with_quotes()
    )
    return c


def orginize_bar() -> Bar:
    o_x = list(s_data.orginations.values())
    o_y = list(s_data.orginations_nums.values())
    c = (
        Bar()
            .add_xaxis(o_x)
            .add_yaxis("机构", o_y, category_gap="60%")
            .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "color": JsCode(
                        """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 122, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""
                    ),
                    "barBorderRadius": [30, 30, 30, 30],
                    "shadowColor": "rgb(0, 160, 221)",
                }
            }
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="机构"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        )
            .dump_options_with_quotes()
    )
    return c


def year_line():
    x = [str(i) for i in list(s_data.year_num.values())]
    y_data = list(s_data.year_data.values())

    line2 = (
        Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(opacity=1, color="#C67570"),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
            # 设置 boundary_gap 的时候一定要放在最后一个配置项里, 不然会被覆盖
            .dump_options_with_quotes()
    )
    return line2


def xueke_pie():
    data1 = list(s_data.xueke_ditc.values())
    data2 = list(s_data.xueke_nums.values())
    c = (
        Pie()
            .add(
            "",
            [
                list(z)
                for z in zip(
                data1,
                data2,
            )
            ],
            center=["40%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各学科占比"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .dump_options_with_quotes()
    )
    return c


def qikan_bar() -> Bar:
    x = list(reversed((list(s_data.qikan_dict.values()))))
    y = list(reversed(list(s_data.qikan_nums.values())))
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("期刊", y)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="期刊数量展示"))
            .dump_options_with_quotes()
    )
    return c


def cat_pie():
    data1 = s_data.cat
    data2 = s_data.cat_nums
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(data1, data2)],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="资源类型展示"))
            .dump_options_with_quotes()
    )
    return c


def wordshow():
    data1 = list(s_data.keywords.values())
    data2 = list(s_data.keywords_nums.values())

    c = (
        Bar()
            .add_xaxis(data1)
            .add_yaxis("关键词", data2)
            .set_series_opts(label_opts=opts.LabelOpts(position="top"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="词频展示"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        )
            .dump_options_with_quotes()
    )
    return c


def relation():
    nodes = [
        {"name": "邢蓓蓓", "symbolSize": 10},
        {"name": "林剑", "symbolSize": 20},
        {"name": "武敬平", "symbolSize": 30},
        {"name": "陶锋", "symbolSize": 40},
        {"name": "宋振峰", "symbolSize": 50},
        {"name": "胡伟", "symbolSize": 40},
        {"name": "吴小龙", "symbolSize": 30},
        {"name": "喻小勇", "symbolSize": 20},
    ]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get("name"), "target": j.get("name")})
    c = (
        Graph()
            .add("", nodes, links, repulsion=8000)
            .set_global_opts(title_opts=opts.TitleOpts(title="关系图"))
            .dump_options_with_quotes()
    )
    return c


class AuthorChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(author_bar()))


class OrginiseChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(orginize_bar()))


class YearChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(year_line()))


class XuekeChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(xueke_pie()))


class QikanChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(qikan_bar()))


class CatChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(cat_pie()))


class WordChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(wordshow()))


class RelationChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(relation()))

@method_decorator([login_required(login_url='/user/login/'),],name='dispatch')
class ShowView(APIView):
    def get(self, request, *args, **kwargs):
        documents = Document.objects.all()
        author_lists = []
        for d in documents:
            author_lists.append(d.author)
        print(author_lists)
        return HttpResponse(content=open("./templates/front/show.html", encoding="utf-8").read())


@login_required(login_url='/user/login/')
def upper_search(request):
    searchtype1 = request.GET.get('searchtype1')

    upper_words1 = request.GET.get('upper_words1')
    searchtype_logic = request.GET.get('searchtype_logic')
    searchtype2 = request.GET.get('searchtype2')
    upper_words2 = request.GET.get('upper_words2')

    print("searchtype1", searchtype1)
    print("searchtype2", searchtype2)
    print("searchtype_logic", searchtype_logic)
    print("upper_words1", upper_words1)
    print("upper_words2", upper_words2)

    if upper_words1 and upper_words2:
        if searchtype_logic == 'and':
            print('and')
            if searchtype1 == 'author' and searchtype2 == 'title':
                documents = Document.objects.filter(author__icontains=upper_words1, title__icontains=upper_words2).all()
            elif searchtype1 == 'author' and searchtype2 == 'keywords':
                documents = Document.objects.filter(author__icontains=upper_words1,
                                                    key_words__icontains=upper_words2).all()
            elif searchtype1 == 'author' and searchtype2 == 'summary':
                documents = Document.objects.filter(author__icontains=upper_words1,
                                                    summary__icontains=upper_words2).all()
            elif searchtype1 == 'title' and searchtype2 == 'keywords':
                documents = Document.objects.filter(title__icontains=upper_words1,
                                                    key_words__icontains=upper_words2).all()
            elif searchtype1 == 'keywords' and searchtype2 == 'summary':
                documents = Document.objects.filter(key_words__icontains=upper_words1,
                                                    summary__icontains=upper_words2).all()
            elif searchtype1 == 'title' and searchtype2 == 'summary':
                documents = Document.objects.filter(key_words__icontains=upper_words1,
                                                    summary__icontains=upper_words2).all()
            else:
                documents = Document.objects.filter().all()
            print("documents", documents)
            context = {
                'documents': documents,
            }
            return render(request, 'front/search.html', context=context)

        elif searchtype_logic == 'or':
            print('or')
            if searchtype1 == 'author' and searchtype2 == 'title':
                documents = Document.objects.filter(
                    Q(author__icontains=upper_words1) | Q(title__icontains=upper_words2)).all()
            elif searchtype1 == 'author' and searchtype2 == 'keywords':
                documents = Document.objects.filter(
                    Q(author__icontains=upper_words1) | Q(key_words__icontains=upper_words2)).all()
            elif searchtype1 == 'author' and searchtype2 == 'summary':
                documents = Document.objects.filter(
                    Q(author__icontains=upper_words1) | Q(summary__icontains=upper_words2)).all()
            elif searchtype1 == 'title' and searchtype2 == 'keywords':
                documents = Document.objects.filter(
                    Q(title__icontains=upper_words1) | Q(key_words__icontains=upper_words2)).all()
            elif searchtype1 == 'keywords' and searchtype2 == 'summary':
                documents = Document.objects.filter(
                    Q(key_words__icontains=upper_words1) | Q(summary__icontains=upper_words2)).all()
            elif searchtype1 == 'title' and searchtype2 == 'summary':
                documents = Document.objects.filter(
                    Q(title__icontains=upper_words1) | Q(summary__icontains=upper_words2)).all()
            else:
                documents = Document.objects.filter().all()
            print("documents",documents)
            context = {
                'documents': documents,
            }
            return render(request, 'front/search.html', context=context)
    else:
        documents = Document.objects.filter().all()

        context = {
            'documents': documents,
        }
        return render(request, 'front/search.html', context=context)


def test(request):
    upper_words1 = request.GET.get('upper_words1')
    upper_words2 = request.GET.get('upper_words2')

    documents = Document.objects.filter(Q(title__contains=upper_words1) | Q(key_words__contains=upper_words2)).all()

    for d in documents:
        print(d.title)
        print(d.key_words)

    context = {
        "documents":documents
    }
    return render(request,'front/search.html',context=context)


