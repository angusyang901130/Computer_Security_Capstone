#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>	
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUF_SIZE 1024

int main(int argc, char* argv[]){

    struct sockaddr_in serv;
    bzero(&serv, sizeof(serv));

    ssize_t rlen, wlen;

    int fd = socket(AF_INET, SOCK_STREAM, 0);

    char* ip = argv[1];
    serv.sin_addr.s_addr = inet_addr(ip);
    serv.sin_port = htons(atoi(argv[2]));
    serv.sin_family = AF_INET;

    if(connect(fd, (struct sockaddr*)&serv, sizeof(serv)) < 0)
        perror("connect");

    char buf[BUF_SIZE];

    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    char ans[] = "-1\n";

    wlen = write(fd, ans, strlen(ans));

    bzero(buf, BUF_SIZE);

    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    close(fd);

}