import os


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def create_project_directory(project_name):
    if not os.path.exists(project_name):
        print('\nCreating {}/ project directory'.format(project_name))
        os.makedirs(project_name)


def create_project_files(project_name, base_url):
    queue_path = os.path.join(project_name, 'queue.txt')
    crawled_path = os.path.join(project_name, 'crawled.txt')

    if not os.path.isfile(queue_path):
        print('Creating {}'.format(queue_path))
        # adding base_url to queue
        write_file(queue_path, base_url)

    if not os.path.isfile(crawled_path):
        print('Creating {}'.format(crawled_path))
        # on setup there's no crawled links
        write_file(crawled_path, '')

    else:
        print('\nLoading previous search state')


def file_to_set(path):
    """
    converts file to set
    """
    data_set = set()
    with open(path, 'r') as f:
        for line in f:
            data_set.add(line.replace('\n', ''))
    return data_set


def set_to_file(data_set, path):
    """
    converts set to file
    """
    with open(path, 'w') as f:
        for link in sorted(data_set):
            f.write(link + '\n')
