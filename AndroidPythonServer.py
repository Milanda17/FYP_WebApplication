import socket

from RealTimeRec import RealTimeRecomandationClass


def recv():
    host, port = "192.168.43.50",3305
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.bind((host, port))
    finally:
        pass
    client.listen(10)  # how many connections can it receive at one time
    print("Start Listening...")

    while True:

        conn, addr = client.accept()
        data = conn.recv(3305)
        converData= data.decode("utf-8")




        if converData == "Iamconnect":
            reply = "Success"
            conn.send(reply.encode("utf-8"))
            print("Successfully connected ");
            conn.close()


        else:

            messagePart = converData.split("#")
            #print(messagePart[1]) # item list came from mobile
            #print(messagePart[0])  # user id
            itemInCart = list(messagePart[1].split(","))



            sendItemRecon=itemRecommendation(itemInCart,messagePart[0])
            sendRecipes=recipesRecommendation();

            sendMessage=""
            sendMessage=sendMessage+sendItemRecon;
            sendMessage=sendMessage+"#"
            sendMessage=sendMessage+sendRecipes
            conn.send(sendMessage.encode("utf-8"))

            print("this is full reply send to mobile===>",sendMessage)
            conn.close()


    client.close()



def itemRecommendation(itemInCart,customerId):
    print("in cart",itemInCart)
    objRealTimeRecomandationClass = RealTimeRecomandationClass()
    recom = objRealTimeRecomandationClass.start(itemInCart, customerId)

    itemRecomString = ','.join([str(elem) for elem in recom])

    print("Item send to android =====> ",itemRecomString)




    return itemRecomString


def recipesRecommendation():


    recipesReconString="mearge with the madhus part "



    return recipesReconString


if __name__ == '__main__':


    recv()


