import os


def compile_file_to_txt(filename, folder_name):
    os.system("atop -r uploads/{0}/{1} > uploads/{0}/{1}.txt".format(folder_name, filename))
    os.system("atop -r uploads/{0}/{1} -c > uploads/{0}/{1}_c.txt".format(folder_name, filename))
    os.system("atop -r uploads/{0}/{1} -m > uploads/{0}/{1}_mem.txt".format(folder_name, filename))
    os.system("atop -r uploads/{0}/{1} -m -c > uploads/{0}/{1}_mem_c.txt".format(folder_name, filename))
    os.system("atop -r uploads/{0}/{1} -d > uploads/{0}/{1}_dsk.txt".format(folder_name, filename))
    os.system("atop -r uploads/{0}/{1} -d -c > uploads/{0}/{1}_dsk_c.txt".format(folder_name, filename))


def parse_cpu(filename, folder_name):

    with open('uploads/{0}/{1}.txt'.format(folder_name, filename), 'r') as cpu_file:
        atop_file = cpu_file
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
        general_cpu_sys_list = []
        general_cpu_user_list = []
        for line in atop_file:
            line = line.split()
            try:
                if line[0] == 'ATOP':
                    date = str(line[3]+' '+line[4])
                if line[0] == 'cpu':
                    if line[2] == 'sys':
                        general_cpu_sys = line[3][:-1]
                        process_data_dict = dict({"date": date, "count": general_cpu_sys})
                        general_cpu_sys_list.append(process_data_dict)
                    if line[5] == 'user':
                        general_cpu_user = line[6][:-1]
                        process_data_dict = dict({"date": date, "count": general_cpu_user})
                        general_cpu_user_list.append(process_data_dict)
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

    with open('uploads/{0}/{1}_c.txt'.format(folder_name, filename), 'r') as cpu_file_c:
        atop_file_c = cpu_file_c

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

        return [java_list, mongo_list, correlator_list, wafd_list, wafgowaf_list, celery_list, rabbitmq_list, freshclam_list, waf_nginx_list, waf_sync_list, general_cpu_sys_list, general_cpu_user_list]


def parse_mem(filename, folder_name):
    with open('uploads/{0}/{1}_mem.txt'.format(folder_name, filename), 'r') as mem_file:
        atop_file = mem_file

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
        general_mem_total = []
        general_mem_free = []

        for line in atop_file:
            line = line.split()
            try:
                if line[0] == 'ATOP':
                    date = str(line[3]+' '+line[4])
                if line[0] == 'MEM':
                    if line[3][-1] == 'M':
                        m_t = '{:.2f}'.format(float(line[3][:-1]) / 1024)
                        process_data_dict = dict({"date": date, "count": m_t})
                        general_mem_total.append(process_data_dict)
                    else:
                        m_t = float(line[3][:-1])
                        process_data_dict = dict({"date": date, "count": m_t})
                        general_mem_total.append(process_data_dict)

                    if line[6][-1] == 'M':
                        m_f = '{:.2f}'.format(float(line[6][:-1]) / 1024)
                        process_data_dict = dict({"date": date, "count": m_f})
                        general_mem_free.append(process_data_dict)
                    else:
                        m_f = float(line[6][:-1])
                        process_data_dict = dict({"date": date, "count": m_f})
                        general_mem_free.append(process_data_dict)
                if line[-1] == 'java':
                    java_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": java_mem})
                    java_list.append(process_data_dict)
                if line[-1] == 'mongod':
                    mongo_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": mongo_mem})
                    mongo_list.append(process_data_dict)
                if line[-1] == 'wafd':
                    wafd_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": wafd_mem})
                    wafd_list.append(process_data_dict)
                if line[-1] == 'waf-gowaf':
                    wafgowaf_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": wafgowaf_mem})
                    wafgowaf_list.append(process_data_dict)
                if line[-1] == 'celery':
                    celery_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": celery_mem})
                    celery_list.append(process_data_dict)
                if line[-1] == 'beam.smp':
                    rabbitmq_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": rabbitmq_mem})
                    rabbitmq_list.append(process_data_dict)
                if line[-1] == 'freshclam':
                    freshclam_mem = int(line[8][:-1])
                    process_data_dict = dict({"date": date, "count": freshclam_mem})
                    freshclam_list.append(process_data_dict)
            except IndexError:
                pass

    with open('uploads/{0}/{1}_mem_c.txt'.format(folder_name, filename), 'r') as mem_file_c:
        atop_file_c = mem_file_c

        for line in atop_file_c:
            try:
                if line.split()[0] == 'ATOP':
                    date = str(line.split()[3] + ' ' + line.split()[4])
                if 'waf-nginx: worker process' in line:
                    waf_nginx_mem = line.split()[3][:-1]
                    process_data_dict = dict({"date": date, "count": waf_nginx_mem})
                    waf_nginx_list.append(process_data_dict)
                line = line.split()
                if line[-1] == 'waf-sync':
                    waf_sync_mem = line[3][:-1]
                    process_data_dict = dict({"date": date, "count": waf_sync_mem})
                    waf_sync_list.append(process_data_dict)
                if line[-1] == 'waf-correlator':
                    correlator_mem = line[3][:-1]
                    process_data_dict = dict({"date": date, "count": correlator_mem})
                    correlator_list.append(process_data_dict)
            except IndexError:
                pass

        return [java_list, mongo_list, correlator_list, wafd_list, wafgowaf_list, celery_list, rabbitmq_list, freshclam_list, waf_nginx_list, waf_sync_list, general_mem_total, general_mem_free]


def parse_dsk(filename, folder_name):
    with open('uploads/{0}/{1}_dsk.txt'.format(folder_name, filename), 'r') as dsk_file:
        atop_file = dsk_file

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
                    date = str(line[3] + ' ' + line[4])
                if line[-1] == 'java':
                    java_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": java_dsk})
                    java_list.append(process_data_dict)
                if line[-1] == 'mongod':
                    mongo_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": mongo_dsk})
                    mongo_list.append(process_data_dict)
                if line[-1] == 'wafd':
                    wafd_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": wafd_dsk})
                    wafd_list.append(process_data_dict)
                if line[-1] == 'waf-gowaf':
                    wafgowaf_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": wafgowaf_dsk})
                    wafgowaf_list.append(process_data_dict)
                if line[-1] == 'celery':
                    celery_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": celery_dsk})
                    celery_list.append(process_data_dict)
                if line[-1] == 'beam.smp':
                    rabbitmq_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": rabbitmq_dsk})
                    rabbitmq_list.append(process_data_dict)
                if line[-1] == 'freshclam':
                    freshclam_dsk = int(line[5][:-1])
                    process_data_dict = dict({"date": date, "count": freshclam_dsk})
                    freshclam_list.append(process_data_dict)
            except IndexError:
                pass

    with open('uploads/{0}/{1}_dsk_c.txt'.format(folder_name, filename), 'r') as dsk_file_c:
        atop_file_c = dsk_file_c

        for line in atop_file_c:
            try:
                if line.split()[0] == 'ATOP':
                    date = str(line.split()[3] + ' ' + line.split()[4])
                if 'waf-nginx: worker process' in line:
                    waf_nginx_dsk = line.split()[3][:-1]
                    process_data_dict = dict({"date": date, "count": waf_nginx_dsk})
                    waf_nginx_list.append(process_data_dict)
                line = line.split()
                if line[-1] == 'waf-sync':
                    waf_sync_dsk = line[3][:-1]
                    process_data_dict = dict({"date": date, "count": waf_sync_dsk})
                    waf_sync_list.append(process_data_dict)
                if line[-1] == 'waf-correlator':
                    correlator_dsk = line[3][:-1]
                    process_data_dict = dict({"date": date, "count": correlator_dsk})
                    correlator_list.append(process_data_dict)
            except IndexError:
                pass

        return [java_list, mongo_list, correlator_list, wafd_list, wafgowaf_list, celery_list, rabbitmq_list,
                freshclam_list, waf_nginx_list, waf_sync_list]