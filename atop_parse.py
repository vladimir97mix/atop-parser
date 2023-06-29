import os


def compile_file_to_txt(filename):
    os.system("atop -r uploads/{0} > uploads/{1}.txt".format(filename, filename))


def parse_cpu(filename):

    atop_file = open('uploads/{0}.txt'.format(filename), 'r')
    # atop_file = open('uploads/atop.txt', 'r')

    date = ''
    java_cpu_list = []
    mongo_cpu_list = []
    correlator_cpu_list = []
    wafd_cpu_list = []
    wafgowaf_cpu_list = []
    celery_cpu_list = []
    rabbitmq_cpu_list = []
    freshclam_cpu_list = []
    waf_nginx_cpu_list = []

    for line in atop_file:
        line = line.split()
        # print(line)
        try:
            if line[0] == 'ATOP':
                date = str(line[3]+' '+line[4])
            if line[-1] == 'java':
                java_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": java_cpu})
                java_cpu_list.append(process_data_dict)
            if line[-1] == 'mongod':
                mongo_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": mongo_cpu})
                mongo_cpu_list.append(process_data_dict)
            if line[-1] == 'pidtwistd.py':
                correlator_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": correlator_cpu})
                correlator_cpu_list.append(process_data_dict)
            if line[-1] == 'wafd':
                wafd_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": wafd_cpu})
                wafd_cpu_list.append(process_data_dict)
            if line[-1] == 'waf-gowaf':
                wafgowaf_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": wafgowaf_cpu})
                wafgowaf_cpu_list.append(process_data_dict)
            if line[-1] == 'celery':
                celery_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": celery_cpu})
                celery_cpu_list.append(process_data_dict)
            if line[-1] == 'beam.smp':
                rabbitmq_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": rabbitmq_cpu})
                rabbitmq_cpu_list.append(process_data_dict)
            if line[-1] == 'freshclam':
                freshclam_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": freshclam_cpu})
                freshclam_cpu_list.append(process_data_dict)
            if line[-1] == 'waf-nginx':
                waf_nginx_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": waf_nginx_cpu})
                waf_nginx_cpu_list.append(process_data_dict)

        except IndexError:
            pass
    atop_file.close()
    return [java_cpu_list, mongo_cpu_list, correlator_cpu_list, wafd_cpu_list, wafgowaf_cpu_list, celery_cpu_list, rabbitmq_cpu_list, freshclam_cpu_list, waf_nginx_cpu_list]


# def parse_mongo_cpu(filename):
#     atop_file = open('uploads/{0}.txt}'.format(filename), 'r')
#
#     date = ''
#     mongo_cpu_list = []
#
#     for line in atop_file:
#         line = line.split()
#         # print(line)
#         try:
#             if line[0] == 'ATOP':
#                 date = str(line[3] + ' ' + line[4])
#             if line[-1] == 'mongod':
#                 mongo_cpu = int(line[10][:-1])
#                 process_data_dict = dict({"date": date, "count": mongo_cpu})
#                 mongo_cpu_list.insert(0, process_data_dict)
#
#         except IndexError:
#             pass
#     atop_file.close()
#     return mongo_cpu_list


def parse_correlator_cpu():
    #pidtwistd.py
    pass


def parse_wafd_cpu():
    pass


def parse_wafgowaf_cpu():
    pass


def parse_celery_cpu():
    pass


def parse_rabbitmq_cpu():
    #beam.smp
    pass


