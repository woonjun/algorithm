#include "Common.h"

#define BUFSIZE    512
#pragma comment(lib, "ws2_32.lib")

int main(int argc, char *argv[])
{	
	if (argc != 3)
	{
		printf("Usage : %s <port> <clientIP>\n", argv[0]);
		exit(1);
	}

	char* WhiteListIP = argv[2];
	const char* WrongMSG = "Wrong Client";
	const char* WelcomeMSG = "Hello";

	int retval;

	// ���� �ʱ�ȭ
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		return 1;

	// ���� ����
	SOCKET listen_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (listen_sock == INVALID_SOCKET) err_quit("socket()");

	// bind()
	struct sockaddr_in serveraddr;
	memset(&serveraddr, 0, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons(atoi(argv[1]));
	retval = bind(listen_sock, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
	if (retval == SOCKET_ERROR) err_quit("bind()");

	// listen()
	retval = listen(listen_sock, SOMAXCONN);
	if (retval == SOCKET_ERROR) err_quit("listen()");

	// ������ ��ſ� ����� ����
	SOCKET client_sock;
	struct sockaddr_in clientaddr;
	int addrlen;
	char buf[BUFSIZE + 1];


	while (1) {

		// accept()
		addrlen = sizeof(clientaddr);
		client_sock = accept(listen_sock, (struct sockaddr *)&clientaddr, &addrlen); 
		if (client_sock == INVALID_SOCKET) {
			err_display("accept()");
			break;
		}

		// ������ Ŭ���̾�Ʈ IP Ȯ��
		if (strcmp(inet_ntoa(clientaddr.sin_addr), argv[2]) != 0) {
			// ������ ���� Ŭ���̾�Ʈ
			send(client_sock, WrongMSG, strlen(WrongMSG), 0);
			closesocket(client_sock);
		}else {
			// ������ Ŭ���̾�Ʈ ���� ���
			char addr[INET_ADDRSTRLEN];
			char* ip = inet_ntoa(clientaddr.sin_addr);
			printf("Client IP: %s\n", ip);

			printf("\n[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ ��ȣ=%d\n",
				addr, ntohs(clientaddr.sin_port));
			
			//Hello Ŭ���̾�Ʈ���� send
			send(client_sock, WelcomeMSG, strlen(WelcomeMSG), 0);

			// Ŭ���̾�Ʈ�� ������ ���
			int received = 0;
			while (1) {
				// ������ �ޱ�
				retval = recv(client_sock, buf, BUFSIZE, 0);
				if (retval == SOCKET_ERROR) {
					err_display("recv()");
					break;
				}
				else if (retval == 0)
					break;

				// ���� ������ ���
				buf[retval] = '\0';
				printf("[TCP/%s:%d] %s\n", addr, ntohs(clientaddr.sin_port), buf);

				// ���� ����Ʈ ���� Ŭ���̾�Ʈ���� ȸ��
				received += retval;
				snprintf(buf, BUFSIZE, "%d", retval);

				// ������ ������
				retval = send(client_sock, buf, strlen(buf), 0);
				if (retval == SOCKET_ERROR) {
					err_display("send()");
					break;
				}

			}
			printf("[TCP ����] Ŭ���̾�Ʈ ����: IP �ּ�=%s, ��Ʈ ��ȣ=%d\n",
				addr, ntohs(clientaddr.sin_port));
			printf("[TCP ����] �� ���� ����Ʈ�� : %d\n", received);

			// ���� �ݱ�
			//closesocket(client_sock);
		}

	}
	// ���� �ݱ�
	closesocket(listen_sock);

	// ���� ����
	WSACleanup();
	return 0;
}
