import certifi
from pymongo import MongoClient

url="mongodb+srv://merteren3663:mert2001eren@cluster0.wstc18x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

ca=certifi.where()

client=MongoClient(url,tlsCAFile=ca)


def addUser(username,password):
    
    cursor=client.first_bd.User.find({'username':username})
    if len(cursor.to_list())!=0:
        return 0
    newUser={'username':username,'password':password,'rates':[],'reviews':[]}
    client.first_bd.User.insert_one(newUser)
    return 1

def deleteAccountFromDatabase(username):
    cursor=client.first_bd.User.find({'username':username})
    if len(cursor.to_list())==0:
        return 0
    liste=client.first_bd.Product.find().to_list()
    for prod in liste:
        fList=[]
        fListR=[]
        queryp={'name':prod['name']}
        for elem in prod['reviews']:
            if elem['username']!=username:
                fList.append(elem)
        updatep={'$set':{'reviews':fList}}
        for elem in prod['rates']:
            if elem['username']!=username:
                fListR.append(elem)
        updatepR={'$set':{'rates':fListR}}
        client.first_bd.Product.find_one_and_update(queryp,updatep)
        client.first_bd.Product.find_one_and_update(queryp,updatepR)
    client.first_bd.User.delete_one({'username':username})
    return 1

def deleteProductFromDatabase(pname):
    cursor=client.first_bd.Product.find({'name':pname})
    if len(cursor.to_list())==0:
        return 0
    liste=client.first_bd.User.find().to_list()
    for user in liste:
        fList=[]
        fListR=[]
        queryp={'username':user['username']}
        for elem in user['reviews']:
            if elem['pName']!=pname:
                fList.append(elem)
        for elem in user['rates']:
            if elem['pName']!=pname:
                fList.append(elem)
        updatep={'$set':{'reviews':fList}}
        updatepR={'$set':{'rates':fListR}}
        client.first_bd.User.find_one_and_update(queryp,updatep)
        client.first_bd.User.find_one_and_update(queryp,updatepR)
    client.first_bd.Product.delete_one({'name':pname})
    return 1


def isCredentialsCorrect(username,password):
    cursor=client.first_bd.User.find({'username':username,'password':password})
    if len(cursor.to_list())!=0:
        return 1
    return 0


def showUser(username):
    cursor=client.first_bd.User.find({'username':username})
    liste=cursor.to_list()
    return liste[0]

def rate(pname,point,uname):
    p=int(point)
    update={'$push':{'rates':{'username':uname,'point':point}}}
    query={'name':pname}
    updateu={'$push':{'rates':{'pName':pname,'point':point}}}
    queryu={'username':uname}
    product=client.first_bd.Product.find_one_and_update(query,update)
    product=client.first_bd.User.find_one_and_update(queryu,updateu)
    return

def review(name,comment,uname):
    update={'$push':{'reviews':{'username':uname,'comment':comment}}}
    query={'name':name}
    updateu={'$push':{'reviews':{'pName':name,'comment':comment}}}
    queryu={'username':uname}
    product=client.first_bd.Product.find_one_and_update(query,update)
    product=client.first_bd.User.find_one_and_update(queryu,updateu)
    return



def addProducttodb(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10):
    if a1=="" or a2=="" or a3=="" or a4=="" or a5=="":
        return 1
    cursor=client.first_bd.User.find({'name':a1})
    if len(cursor.to_list())!=0:
        return 2
    element={'name':a1,'description':a2,'price':a3,'seller':a4,'image':a5,'category':a10,'rates':[],'reviews':[]}
    match a10:
        case "Antique Furniture":
            if a7=="" or a9=="":
                return 3
            element['age']=a7
            element['material']=a9
        case "Vinyls":
            if a7=="":
                return 3
            element['age']=a7
        case "GPS Sport Watch":
            if a6=="":
                return 3
            element['battery_life']=a6
        case "Sport Shoe":
            if a8=="" or a9=="":
                return 3
            element['size']=a8
            element['material']=a9
        case _:
            return 4
    client.first_bd.Product.insert_one(element)
    return 0


def listAllProducts():
    return client.first_bd.Product.find().to_list()

def showProduct(name):
    productList=client.first_bd.Product.find({'name':name}).to_list()
    if len(productList)>0:
        return client.first_bd.Product.find({'name':name}).to_list()[0]
    return {}

