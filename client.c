#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
 
int main(int argc, char *argv[])
{
  int sockfd = 0,n = 0;
  char recvBuff[1024];
  struct sockaddr_in serv_addr;
  char sendBuff[1024]; 

  struct hostent *hen;

  memset(recvBuff, '0' ,sizeof(recvBuff));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }

  hen=gethostbyname(argv[1]);
 
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(atoi(argv[2]));
  //serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
  
  bcopy((char *)hen->h_addr,(char *)&serv_addr.sin_addr.s_addr,hen->h_length); 

  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
 
// Commented out for now. 
/* while((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0)
    {
      recvBuff[n] = 0;
      if(fputs(recvBuff, stdout) == EOF)
    {
      printf("\n Error : Fputs error");
    }
      printf("\n");
    }
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
*/
  
 // strcpy(sendBuff, "Test message from client");

  fgets(sendBuff, sizeof(sendBuff), stdin);
  write(sockfd, sendBuff, strlen(sendBuff));

  return 0;
}
