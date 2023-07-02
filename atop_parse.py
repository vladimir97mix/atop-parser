import os


# def compile_file_to_txt(filename):
#     os.system("atop -r uploads/{0} > uploads/{1}.txt".format(filename, filename))
#     os.system("atop -r uploads/{0} -c > uploads/{1}_c.txt".format(filename, filename))

# def parse_cpu():
#     atop_file = open('uploads/atop.txt', 'r')

def parse_cpu(filename):
    # compile_file_to_txt(filename)

    # atop_file = open('uploads/{0}.txt'.format(filename), 'r')
    atop_file = open('uploads/atop.txt', 'r')

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
    waf_sync_cpu_list = []
    for line in atop_file:
        line = line.split()
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
        except IndexError:
            pass
    atop_file.close()

    atop_file = open('uploads/atop_c.txt', 'r')
    # atop_file = open('uploads/{0}_c.txt'.format(filename), 'r')
    for line in atop_file:
        try:
            if line.split()[0] == 'ATOP':
                date = str(line.split()[3] + ' ' + line.split()[4])
            if 'waf-nginx: worker process' in line:
                waf_nginx_cpu = line.split()[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_nginx_cpu})
                waf_nginx_cpu_list.append(process_data_dict)
            line = line.split()
            if line[-1] == 'waf-sync':
                waf_sync_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": waf_sync_cpu})
                waf_sync_cpu_list.append(process_data_dict)
            if line[-1] == 'waf-correlator':
                correlator_cpu = line[3][:-1]
                process_data_dict = dict({"date": date, "count": correlator_cpu})
                correlator_cpu_list.append(process_data_dict)
        except IndexError:
            pass
    atop_file.close()

    return [java_cpu_list, mongo_cpu_list, correlator_cpu_list, wafd_cpu_list, wafgowaf_cpu_list, celery_cpu_list, rabbitmq_cpu_list, freshclam_cpu_list, waf_nginx_cpu_list, waf_sync_cpu_list]

