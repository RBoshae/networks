#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
 
int main(void)
{
  int listenfd = 0,connfd = 0;

  char recvBuff[1024];
  int n; // Added
  
  struct sockaddr_in serv_addr;
 
  char sendBuff[1025];  
  int numrv;  
 
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  printf("socket retrieve success. Good job!\n");
  
  memset(&serv_addr, '0', sizeof(serv_addr));
  memset(sendBuff, '0', sizeof(sendBuff));
      
  serv_addr.sin_family = AF_INET;    
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
  serv_addr.sin_port = htons(5000);    
 
  bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));
  
  if(listen(listenfd, 10) == -1){
      printf("Failed to listen\n");
      return -1;
  }
     
  
  while(1)
    {
      
      connfd = accept(listenfd, (struct sockaddr*)NULL ,NULL); // accept awaiting request
  
      // Added Code from client.c file
      while((n = read(connfd, sendBuff, sizeof(sendBuff)-1)) > 0)
      {
      sendBuff[n] = 0;
      if(fputs(sendBuff, stdout) == EOF)
      {
      printf("\n Error : Fputs error");
      }
      printf("\n");
      }

      if( n < 0)
      {
      printf("\n Read Error \n");
      }

      // End of Added Code from client.c file


      // strcpy(sendBuff, "Message from server33");
      // write(connfd, sendBuff, strlen(sendBuff));
 
      close(connfd);    
      sleep(1);
    }
 
 
  return 0;
}
