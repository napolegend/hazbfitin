import client


def main():
    c = client.Client(input("Nickname: "), input("IP: "), input("[+] AES key: "))
    client.run_client(c)


if __name__ == '__main__':
    main()
