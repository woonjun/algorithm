#define _WINSOCK_DEPRECATED_NO_WARNINGS
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#pragma comment(lib, "ws2_32");
void ErrorHandling(char* message);

int main(int argc, char* argv[])
{
    WSADATA wsaData;
    SOCKET hSocket;
    SOCKADDR_IN servAddr;
    char message[100];
    char sendBuffer[100];
    int strLen = 0;

    if (argc != 3) {
        printf("Usage : %s <Server IP> <Server Port>\n", argv[0]);
        exit(1);
    }

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
        ErrorHandling("WSAStartup() error!");

    hSocket = socket(PF_INET, SOCK_STREAM, 0);
    if (hSocket == INVALID_SOCKET)
        ErrorHandling("socket() error");

    memset(&servAddr, 0, sizeof(servAddr));
    servAddr.sin_family = AF_INET;
    servAddr.sin_addr.s_addr = inet_addr(argv[1]);
    servAddr.sin_port = htons(atoi(argv[2]));

    if (connect(hSocket, (SOCKADDR*)&servAddr, sizeof(servAddr)) == SOCKET_ERROR)
        ErrorHandling("connect() error");

    // �����κ��� �ʱ� �޽��� ����
    strLen = recv(hSocket, message, sizeof(message) - 1, 0);
    if (strLen == SOCKET_ERROR)
        ErrorHandling("recv() error");

    message[strLen] = '\0';
    printf("Message from server: %s\n", message);

  
    while (1) {
   
        // �޽��� �Է�
        printf("Enter a message (up to 20 Bytes or 'End' to quit): ");
        fgets(message, sizeof(message), stdin);

        // ���� ���ڸ� �� ���ڷ� �����Ͽ� ����
        size_t msgLength = strlen(message);
        if (msgLength > 0 && message[msgLength - 1] == '\n') {
            message[msgLength - 1] = '\0';  
        }

        // ���� ���� Ȯ��
        if (strncmp(message, "End", 3) == 0) {
            send(hSocket, message, 3, 0);
            closesocket(hSocket);
            WSACleanup();
            break;
        }

        // �޽����� 20����Ʈ �̸��� ��� �� ĭ�� '*'�� ä��
        if (strlen(message) <= 20) {
            memset(sendBuffer, '*', 20);  // '*'�� �ʱ�ȭ
            strncpy(sendBuffer, message, strlen(message));  // �Էµ� �޽��� ����
        }

        // �޽����� 20����Ʈ �̻��� ��� �ʰ� �κ��� �߶�
        else {
            strncpy(sendBuffer, message, 20);  // �ִ� 20����Ʈ�� ����
        }

        // ������ �޽��� ����
        strLen = send(hSocket, sendBuffer, 20, 0);
        if (strLen == SOCKET_ERROR) {
            ErrorHandling("send() error");
            break;
        }

        // �����κ��� ���� ����
        strLen = recv(hSocket, message, sizeof(message) - 1, 0);
        if (strLen == SOCKET_ERROR) {
            ErrorHandling("recv() error");
            break;
        }

        message[strLen] = '\0';
        printf("Server replied: %s\n", message);
    }

    return 0;
}

void ErrorHandling(char* message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}
