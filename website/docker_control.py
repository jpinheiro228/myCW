import docker
from docker import APIClient
import os
import json
import re


dir_path = os.path.dirname(os.path.realpath(__file__))
client = docker.from_env()
c_low_level = APIClient(base_url='unix://var/run/docker.sock')


BASEDOCKERFILE = """FROM gcc
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN g++ -o myapp main.c
CMD ["./myapp"]"""

BASEHEADER = """#include<iostream>
using namespace std;"""


def escape_ansi(line):
    """ Remove Control Sequences (aka ANSI Escape Sequences) from lines

    :param line:
    :return:
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def run_tests(tag="container", user="test_user"):
    response = [line for line in c_low_level.build(tag=tag, path=dir_path + "/codes/"+user, rm=True, forcerm=True)]
    for l in response:
        if "error" in l.decode():
            clear_images(tag)
            return escape_ansi(json.loads(l.decode())["stream"])

    try:
        output = escape_ansi(client.containers.run(tag, "/usr/src/myapp/myapp", remove=True, tty=True,
                                                   stdin_open=True).decode())
        client.images.remove(tag)
        return output
    except Exception as e:
        clear_images(tag)
        return escape_ansi("Error in execution: {}".format(e))


def run_code(code, test_code, user):
    if not os.path.isdir(dir_path + "/codes/" + user):
        os.mkdir(dir_path + "/codes/" + user)
        with open(dir_path + "/codes/" + user + "/dockerfile", 'w') as f:
            f.write(BASEDOCKERFILE)

    with open(dir_path + "/codes/" + user + "/main.c", 'w') as f:
        f.write(BASEHEADER)
    with open(dir_path + "/codes/" + user + "/main.c", 'a') as f:
        f.write(code)
        f.write(test_code)
    output = run_tests(user, user)

    clear_images(user)
    return output


def clear_images(tag=None):
    for i in client.images.list():
        if not i.tags:
            client.images.remove(i.id)
        elif tag and tag in i.tags[0].split(":")[0]:
            client.images.remove(tag)


if __name__ == '__main__':
    print(run_tests())

