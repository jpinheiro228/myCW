import docker
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    client = docker.from_env()
    img,json = client.images.build(tag="my-gcc-app", path=dir_path+"/codes/testCode", rm=True)
    try:
        print(client.containers.run("my-gcc-app", "/usr/src/myapp/myapp",remove=True, tty=True, stdin_open=True).decode()) #
    except Exception as e:
        print(e)
    # img.remove()
    # print()
    client.images.remove(img.tags[0].split(":")[0])
