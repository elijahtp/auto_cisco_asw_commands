import paramiko
import time
import socket
from pprint import pprint
import snoop


@snoop
def text_clear(text):
    """Удаление пунктуации"""
    import string

    for p in string.punctuation + "\n":
        if p in text:
            text = text.replace(p, "")
    return text


def counter(list_element):
    """Счетчик повторений элементов последовательности"""
    # создаем словарь, где будем хранить элемент списка в качестве,
    # ключа, а количество его повторений будет значением
    count = {}
    # теперь считаем повторения элементов списка
    for element in list_element:
        if count.get(element, None):
            # если в словаре ключ со значением элемента списка
            # присутствует, то увеличиваем счетчик на 1
            count[element] += 1
        else:
            # если в словаре ключа со значением элемента
            # спитска НЕТ, то создаем ключ со значением 1
            count[element] = 1

    # сортируем словарь по количеству повторений слов в тексте
    sorted_values = sorted(count.items(), key=lambda tpl: tpl[1], reverse=True)
    return dict(sorted_values)


def send_show_command(
    ip,
    username,
    password,
    enable,
    command,
    max_bytes=60000,
    short_pause=1,
    long_pause=5,
):
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    with cl.invoke_shell() as ssh:
        ssh.send("enable\n")
        ssh.send(f"{enable}\n")
        time.sleep(short_pause)
        ssh.send("terminal length 0\n")
        time.sleep(short_pause)
        ssh.recv(max_bytes)
        result = {}
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(3)
            output = ""
            while True:
                try:
                    part = ssh.recv(max_bytes).decode("utf-8")
                    output += part
                    time.sleep(0.5)
                except socket.timeout:
                    break
            result[command] = output
        return result


if __name__ == "__main__":
    indexes_switches_dict = {
        "172.16.99.101": 6,
        "172.16.99.102": 4,
        "172.16.99.103": 3,
        "172.16.99.104": 4,
        "172.16.99.105": 4,
        "172.16.99.106": 4,
        "172.16.99.107": 3,
        "172.16.99.108": 2,
        "172.16.99.109": 2,
        "172.16.99.110": 1,
        "172.16.99.111": 1,
        "172.16.99.112": 1,
        "172.16.99.113": 1,
        "172.16.99.114": 2,
        "172.16.99.115": 1,
        "172.16.99.116": 1,
        "172.16.99.117": 1,
    }
    commands = ["sh int status"]
    for i_s_d_key, i_s_d_item in indexes_switches_dict.items():
        result = send_show_command(i_s_d_key, "user", "password", "password", commands)
        for key, item in result.items():
            resultlist = []
            itemtext = text_clear(item)
            itemlist = itemtext.split()
            itemstring = " ".join(itemlist)
            resultlist.append("{}".format(item))
            resultstring = "; ".join(resultlist)
            print(resultstring[-8:-1])
            print(resultstring[38:-8])
