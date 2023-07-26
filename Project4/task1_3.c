#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>	
#include <stdint.h>
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

    char buf[BUF_SIZE], ans[BUF_SIZE];

    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    char* tmp_buf = strdup(buf);
    char* time_buf = strtok(tmp_buf, ">");
    // printf("%s\n", time_buf);

    char* hour = strtok(time_buf, ":");
    char* min = strtok(NULL, ":");
    char* sec = strtok(NULL, ":");

    // printf("hour: %s\n", hour);
    // printf("min: %s\n", min);
    // printf("sec: %s\n", sec);

    time_t now = time(NULL);
    struct tm *current_time = localtime(&now);

    current_time->tm_hour = atoi(hour);
    current_time->tm_min = atoi(min);
    current_time->tm_sec = atoi(sec);

    // printf("hour: %d\n", current_time->tm_hour);
    // printf("min: %d\n", current_time->tm_min);
    // printf("sec: %d\n", current_time->tm_sec);

    time_t converted_time = mktime(current_time);
    srand((uint32_t)converted_time);


    uint32_t passwd = rand();
    sprintf(ans, "%u\n", passwd);

    wlen = write(fd, ans, strlen(ans));

    bzero(buf, BUF_SIZE);

    rlen = read(fd, buf, BUF_SIZE);
    printf("%s\n", buf);

    close(fd);

}