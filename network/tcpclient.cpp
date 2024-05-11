#include "Common.h"

#define BUFSIZE 20  // �޽����� ���� ���� ũ��
#define INPUTBUFSIZE 512

void err_quit(char* msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

void err_display(char* msg) {
    fprintf(stderr, "%s\n", msg);
}

int main(int argc, char* argv[]) {

   

    if (argc != 3) {
        printf("Usage: %s <Server IP> <port>\n", argv[0]);
        exit(1);
    }

    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) return 1;

    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) err_quit("socket()");

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(atoi(argv[2]));
    if (inet_pton(AF_INET, argv[1], &serveraddr.sin_addr) <= 0) {
        err_quit("Invalid address format");
    }

    if (connect(sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) == SOCKET_ERROR) {
        err_quit("connect()");
    }

    int retval; //���޹��� ����Ʈ ����� ����
    char sendbuf[BUFSIZE + 1]; // 20����Ʈ�� ������ ���� ����, �� ���� ���� ����
    char buf[BUFSIZE + 1];  // BUFSIZE + 1 for null terminator
    char recvbuf[INPUTBUFSIZE + 1];
    char userInputbuf[INPUTBUFSIZE + 1]; //����� fgets�Է�����

    int len = recv(sock, recvbuf, BUFSIZE, 0);
    if (len == SOCKET_ERROR) {
        err_quit("recv() error");
    }

    recvbuf[len] = '\0';

    if (strcmp(recvbuf, "Hello") != 0) {
        printf("[TCP Ŭ���̾�Ʈ] Message from server: %s", recvbuf);
        closesocket(sock);
        WSACleanup();
        return 1;
    }
    else {
        printf("[TCP Ŭ���̾�Ʈ] Message from server: %s", recvbuf);
    }

    // ������ ������ ���
    while (1) {

        // ������ �Է�
        printf("\n[���� ������] ");
        if (fgets(userInputbuf, INPUTBUFSIZE, stdin) == NULL) {// ū ���� ũ��� �Է� �ޱ�
            printf("�Է¿����߻�!");
            break;
        }

        // �Է¹��� ���ڿ����� '\n' ����
        int len = strlen(userInputbuf);
        if (userInputbuf[len - 1] == '\n') {
            userInputbuf[len - 1] = '\0';
            len--; // ���� ����
        }
        printf("������ �Է��� len����: %d\n", len);

        if (len == 0) // �Է��� ������ ���
            continue;

        // "End" �Է� �� Ŭ���̾�Ʈ ����
        if (strcmp(userInputbuf, "End") == 0) {
            printf("[TCP Ŭ���̾�Ʈ] �����մϴ�.\n");
            break;
        }

        // �Էµ� �����Ͱ� 20����Ʈ�� �ʰ��� ��� 20����Ʈ�� �߶󳻱�
        if (len > 20) {
            len = 20; // ���̸� 20���� ����
        }

        // sendbuf�� '#'���� �ʱ�ȭ�ϰ� ������ ����
        memset(sendbuf, '*', 20);
        memcpy(sendbuf, userInputbuf, len);
        sendbuf[20] = '\0'; // ���Ȼ��� ������ NULL ���� ���� ����

        // ������ ������ (��Ȯ�� 20����Ʈ ����)
        retval = send(sock, sendbuf, 20, 0);
        if (retval == SOCKET_ERROR) {
            err_display("send()");
            break;
        }
        printf("[TCP Ŭ���̾�Ʈ] 20����Ʈ�� ���½��ϴ�.\n");

        // �����κ����� ���� �ޱ�
        retval = recv(sock, recvbuf, INPUTBUFSIZE, 0);
        if (retval == SOCKET_ERROR) {
            err_display("recv()");
            break;
        }
        else if (retval == 0) {
            break; // ���� ���� ����
        }

        // ���� ������ ���
        recvbuf[retval] = '\0';
        int receivedByte = atoi(recvbuf);
        printf("[TCPŬ���̾�Ʈ]�����κ��� %s��ŭ ���Ź޾��� \n", recvbuf);
        if (receivedByte == 20) {
            printf("���� ����Ʈ�� �����κ��� ���Ź޾Ҵٰ� �� ����Ʈ�� ��ġ�� \n");
        }
        else {
            printf("���� ����Ʈ�� �����κ��� ���Ź޾Ҵٰ� �� ����Ʈ�� ��ġ���� ����\n");
        }
    }



    closesocket(sock);
    WSACleanup();
    return 0;
}
