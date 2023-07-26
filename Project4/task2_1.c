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

    memset(buf, 0, BUF_SIZE);
    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    // memset(buf, 0, BUF_SIZE);
    // rlen = read(fd, buf, BUF_SIZE);
    // printf("%s\n", buf);

    // unsigned char *ans = "abcdefghabcdefghabcdefgh\x11\x1a\x40\x00\x00\x00\x00\x00abcdefgh\xf5\x17\x40\x00\x00\x00\x00\x00";
    // unsigned char ans[64] = "\x30\x31\x32\x33\x34\x35\x36\x37\x30\x31\x32\x33\x34\x35\x36\x37\x11\x1a\x40\x00\x00\x00\x00\x00\x30\x31\x32\x33\x34\x35\x36\x37\xf5\x17\x40\x00\x00\x00\x00\x00";
    // printf("%s\n", ans);
    // strcat(ans, "\x30\x31\x32\x33\x34\x35\x36\x37");
    // printf("%s\n", ans);
    // strcat(ans, "\x30\x31\x32\x33\x34\x35\x36\x37");
    // printf("%s\n", ans);
    // strcat(ans, "\x30\x31\x32\x33\x34\x35\x36\x37");
    // strcat(ans, "\x30\x31\x32\x33\x34\x35\x36\x37");
    // strcat(ans, "\x11\x1a\x40\x00\x00\x00\x00\x00");
    // strcat(ans, "\x00\x00\x00\x00\x00\x40\x1a\x11");
    // strcat(ans, "\x30\x31\x32\x33\x34\x35\x36\x37");
    // strcat(ans, "\xf5\x17\x40\x00\x00\x00\x00\x00");

    unsigned char ans[48] = "\x30\x31\x32\x33\x34\x35\x36\x37\x30\x31\x32\x33\x34\x35\x36\x37\x30\x31\x32\x33\x34\x35\x36\x37\x11\x1a\x40\x00\x00\x00\x00\x00\x30\x31\x32\x33\x34\x35\x36\x37\xf5\x17\x40\x00\x00\x00\x00\x00";

    wlen = write(fd, ans, 48);
    // printf("wlen: %ld\n", wlen);

    bzero(buf, BUF_SIZE);

    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    close(fd);

}