import os


def compile_file_to_txt(filename):
    os.system("atop -r ./uploads/{0} > ./uploads/{1}.txt".format(filename, filename))
    os.system("atop -r ./uploads/{0} -c > ./uploads/{1}_c.txt".format(filename, filename))
    os.system("atop -r ./uploads/{0} -m > ./uploads/{1}_mem.txt".format(filename, filename))
    os.system("atop -r ./uploads/{0} -m -c > ./uploads/{1}_mem_c.txt".format(filename, filename))


# def parse_cpu(filename):
#     # atop_file = open('uploads/atop.txt', 'r')
#     atop_file = open('uploads/{0}.txt'.format(filename), 'r')
#     atop_file_c = open('uploads/{0}_c.txt'.format(filename), 'r')
#     return parse(atop_file, atop_file_c)
#
#
# def parse_mem(filename):
#     # atop_file = open('uploads/atop_mem.txt', 'r')
#     atop_file = open('uploads/{0}_mem.txt'.format(filename), 'r')
#     atop_file_c = open('uploads/{0}_mem_c.txt'.format(filename), 'r')
#     return parse(atop_file, atop_file_c)


def parse_cpu(filename):

    atop_file = open('uploads/{0}.txt'.format(filename), 'r')

    date = ''
    java_list = []
    mongo_list = []
    correlator_list = []
    wafd_list = []
    wafgowaf_list = []
    celery_list = []
    rabbitmq_list = []
    freshclam_list = []
    waf_nginx_list = []
    waf_sync_list = []
    for line in atop_file:
        line = line.split()
        try:
            if line[0] == 'ATOP':
                date = str(line[3]+' '+line[4])
            if line[-1] == 'java':
                java_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": java_cpu})
                java_list.append(process_data_dict)
            if line[-1] == 'mongod':
                mongo_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": mongo_cpu})
                mongo_list.append(process_data_dict)
            if line[-1] == 'wafd':
                wafd_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": wafd_cpu})
                wafd_list.append(process_data_dict)
            if line[-1] == 'waf-gowaf':
                wafgowaf_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": wafgowaf_cpu})
                wafgowaf_list.append(process_data_dict)
            if line[-1] == 'celery':
                celery_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": celery_cpu})
                celery_list.append(process_data_dict)
            if line[-1] == 'beam.smp':
                rabbitmq_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": rabbitmq_cpu})
                rabbitmq_list.append(process_data_dict)
            if line[-1] == 'freshclam':
                freshclam_cpu = int(line[10][:-1])
                process_data_dict = dict({"date": date, "count": freshclam_cpu})
                freshclam_list.append(process_data_dict)
        except IndexError:
            pass
    atop_file.close()


    atop_file_c = open('uploads/{0}_c.txt'.format(filename), 'r')
    for line in atop_file_c:
        try:
            if line.split()[0] == 'ATOP':
                date = str(line.split()[3] + ' ' + line.split()[4])
            if 'waf-nginx: worker process' in line:
                waf_nginx_cpu = line.split()[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_nginx_cpu})
                waf_nginx_list.append(process_data_dict)
            line = line.split()
            if line[-1] == 'waf-sync':
                waf_sync_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_sync_cpu})
                waf_sync_list.append(process_data_dict)
            if line[-1] == 'waf-correlator':
                correlator_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": correlator_cpu})
                correlator_list.append(process_data_dict)
        except IndexError:
            pass
    atop_file_c.close()

    return [java_list, mongo_list, correlator_list, wafd_list, wafgowaf_list, celery_list, rabbitmq_list, freshclam_list, waf_nginx_list, waf_sync_list]

def parse_mem(filename):

    atop_file = open('uploads/{0}_mem.txt'.format(filename), 'r')

    date = ''
    java_list = []
    mongo_list = []
    correlator_list = []
    wafd_list = []
    wafgowaf_list = []
    celery_list = []
    rabbitmq_list = []
    freshclam_list = []
    waf_nginx_list = []
    waf_sync_list = []
    for line in atop_file:
        line = line.split()
        try:
            if line[0] == 'ATOP':
                date = str(line[3]+' '+line[4])
            if line[-1] == 'java':
                java_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": java_cpu})
                java_list.append(process_data_dict)
            if line[-1] == 'mongod':
                mongo_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": mongo_cpu})
                mongo_list.append(process_data_dict)
            if line[-1] == 'wafd':
                wafd_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": wafd_cpu})
                wafd_list.append(process_data_dict)
            if line[-1] == 'waf-gowaf':
                wafgowaf_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": wafgowaf_cpu})
                wafgowaf_list.append(process_data_dict)
            if line[-1] == 'celery':
                celery_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": celery_cpu})
                celery_list.append(process_data_dict)
            if line[-1] == 'beam.smp':
                rabbitmq_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": rabbitmq_cpu})
                rabbitmq_list.append(process_data_dict)
            if line[-1] == 'freshclam':
                freshclam_cpu = int(line[8][:-1])
                process_data_dict = dict({"date": date, "count": freshclam_cpu})
                freshclam_list.append(process_data_dict)
        except IndexError:
            pass
    atop_file.close()


    atop_file_c = open('uploads/{0}_mem_c.txt'.format(filename), 'r')
    for line in atop_file_c:
        try:
            if line.split()[0] == 'ATOP':
                date = str(line.split()[3] + ' ' + line.split()[4])
            if 'waf-nginx: worker process' in line:
                waf_nginx_cpu = line.split()[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_nginx_cpu})
                waf_nginx_list.append(process_data_dict)
            line = line.split()
            if line[-1] == 'waf-sync':
                waf_sync_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_sync_cpu})
                waf_sync_list.append(process_data_dict)
            if line[-1] == 'waf-correlator':
                correlator_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": correlator_cpu})
                correlator_list.append(process_data_dict)
        except IndexError:
            pass
    atop_file_c.close()

    return [java_list, mongo_list, correlator_list, wafd_list, wafgowaf_list, celery_list, rabbitmq_list, freshclam_list, waf_nginx_list, waf_sync_list]