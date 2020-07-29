from django.shortcuts import render
from .models import Tokenoutput
from django.views.decorators.csrf import csrf_exempt
from konlpy.tag import Okt

import csv, io
from .models import Keywords
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Max, OuterRef, Subquery
from django.http import HttpResponse
from django.utils import timezone


# Create your views here.

text_dicts = []

def token_list(request):

    content = request.POST.get('content')
    if content is None:
        content = ""
    #if 'submit' in request.get:
    #    contents = ''.split(content)

    okt = Okt()
    text = okt.pos(content, norm = True, stem = True)
    output_text1 = [i[0] for i in text if
             ((i[1] not in ['Josa', 'Suffix', 'Punctuation']) &
              (i[0] not in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ',
                            'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅖ', 'ㅐ', 'ㅒ', 'ㅠㅠ', 'ㅠㅠㅠ', 'ㅠㅠㅠㅠ', 'ㅋㅋ', 'ㅋㅋㅋ', 'ㅋㅋㅋㅋ','이','그','저','어느','매우','무척','너무','정말','진짜','되게']))]
    output_text = ' '.join(output_text1)

    output_text_dict = dict(zip(list(range(1, len(output_text1)+1)), output_text1))
    #text_dicts.append(output_text_dict)

    return render(request, 'tokenizer/token_list.html', {'content': content, 'output_text':output_text, 'output_text1':output_text1, 'output_text_dict':output_text_dict})







def select_keywords_first_page(request):
    return select_keywords(request, current_page=1)


def select_keywords(request, current_page):

    # get session_id
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    if request.method == "POST":
        print("POST requested")

        # if method == POST, set current_page = 1
        current_page = 1

        # if method == POST and submit name == submit_upload, insert csv file to database
        if 'submit_upload' in request.POST:
            print("submit_upload")

            # get csv file
            csv_file = request.FILES['file']

            # let's check if it is a csv file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')

            # setup a stream which is when we loop through each line we are able to handle a data in a stream
            io_string = io.StringIO(data_set)
            next(io_string)

            # get max session_index in current session
            # if None, set session_index = 1
            session_index = Keywords.objects.filter(session_id=session_id).aggregate(Max('session_index'))['session_index__max']
            if session_index is None:
                session_index = 1
            else:
                session_index = session_index + 1

            # insert csv to database
            bulk_list = []
            # read csv file
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                # tokenizing with konlpy package
                okt = Okt()
                tokens = okt.pos(column[0], norm=True, stem=True)
                words = [i[0] for i in tokens if
                                ((i[1] not in ['Josa', 'Suffix', 'Punctuation']) &
                                 (i[0] not in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ',
                                               'ㅑ', 'ㅓ', 'ㅕ',
                                               'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅖ', 'ㅐ', 'ㅒ', 'ㅠㅠ', 'ㅠㅠㅠ', 'ㅠㅠㅠㅠ', 'ㅋㅋ', 'ㅋㅋㅋ',
                                               'ㅋㅋㅋㅋ', '이', '그', '저', '어느', '매우', '무척', '너무', '정말', '진짜', '되게']))]
                words = ' '.join(words)
                # create Keywords object and store it in bulk_list
                bulk_list.append(Keywords(session_id=session_id, session_index=session_index, text=column[0], words=words))
                session_index = session_index + 1
            # insert all data to Keywords table at once
            Keywords.objects.bulk_create(bulk_list)

        # if method == POST and submit name == submit_clear, delete all data in current session
        elif 'submit_clear' in request.POST:
            print('submit_clear')
            Keywords.objects.filter(session_id=session_id).delete()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        print("GET requested")
        None

    # set number of data per page
    data_per_page = int(request.GET.get('data', '20'))
    start_data_index = (current_page - 1) * data_per_page + 1
    end_data_index = current_page * data_per_page

    # get total data count in current session
    data_count = Keywords.objects.filter(session_id=session_id).count()
    total_pages = ((data_count - 1) // data_per_page) + 1
    page_list = list(range(total_pages + 1))[1:]

    # get data from database filtered by current session id
    #data = Keywords.objects.filter(session_id=session_id).annotate(row_number=Window(expression=RowNumber(), order_by=F('text').desc())).order_by('row_number')
    sql = 'select a.id, a.created_date, a.updated_date, a.session_id, a.session_index, ' \
          '       a.text, a.words, a.words_selected, coalesce(a.keywords, "") as keywords ' \
          'from tokenizer_keywords a ' \
          'inner join (select id, row_number() over (order by session_index asc) as row_number ' \
          '            from tokenizer_keywords' \
          '            where session_id = "' + session_id + '") b ' \
          'on a.id = b.id ' \
          'where b.row_number >= ' + str(start_data_index) + ' and b.row_number <= ' + str(end_data_index)
    data = Keywords.objects.raw(sql)

    # content is a context variable that can have different values depending on their context
    content = {'data': data,
               'session_id': session_id,
               'page_list': page_list,
               'current_page': current_page,
               'data_per_page': data_per_page
               }

    return render(request, 'tokenizer/select_keywords.html', content)


def ajax_update(request):
    if request.method == 'GET':
        print('ajax_update GET requested')

        keyword = Keywords.objects.get(session_id=request.GET.get('session_id'), session_index=request.GET.get('session_index'))
        keyword.words_selected = request.GET.get('words_selected')
        keyword.keywords = request.GET.get('keywords')
        keyword.updated_date = timezone.now()

        keyword.save()
        return HttpResponse("Success!")

    else:
        print('insertTest GET not requested')
        return HttpResponse("Request method is not a GET")



def export_users_csv(request, session_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keywords.csv"'

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Text', 'Keywords'])

    users = Keywords.objects.filter(session_id=session_id).values_list('text', 'keywords')
    for user in users:
        writer.writerow(user)

    return response