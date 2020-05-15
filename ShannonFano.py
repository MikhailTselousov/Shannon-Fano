#Программа выполняет побуквенное оптимальное кодирование методом Шеннона-Фано для произвольной системы счисления.
#Для использование создайте файл input.txt (utf8 without BOM) и оставьте в нем сообщение. Затем запустите программу и следуйте инструкциям. 
#Результат сохраняется в файл output.txt

def getTotal(arr): #sum up the values every element of an array
    total = 0
    for i in arr:
        total = total + float(i[1])
    return total

def difB2Section(a,b,x,y): #get the intersection of 2 segments: [a, b] & [x, y]
    if b <= x or a >= y:
        return 0
    t1 = a
    t2 = b
    if a<x:
        t1 = x
    if b > y :
        t2 = y
    return t2 - t1 

def sortingMode(arr): #it's key for array.sort(key = key)
    return arr[1]

def encodeThisSegment(info, radix):
    if len(info) <= 1: # if the array length is 1 or 0 then it's done
        return info

    encoded = [] 

    for i in range(0, radix):
        total = getTotal(info)
        portion = total/(radix - i)

        former = 0 #left end and right end of the during element
        latter = 0

        segment = []

        forErase = []
        for ii in range(0, len(info)): #cheking if any element belongs to the during radix segment
            former = latter
            latter = former + float(info[ii][1])

            d1 = difB2Section(former, latter, 0, portion) 
            d2 = difB2Section(former, latter, portion, 2*portion)

            if d1 >= d2 and d1 != 0: #does this element belong to the during radix segment
                segment.append(info[ii]) # if yes then this element goes to separated elements and erases from the source array
                segment[-1][2] = segment[-1][2] + str(i)
                forErase.append(ii) 
        forErase.sort()
        forErase.reverse()

        for ie in forErase:
            info.pop(ie)

        encodedSegment = encodeThisSegment(segment,radix)
        encoded = encoded + encodedSegment  
    
    return encoded

def addToArray(arr, val): #add one more symbol into array of frequency #this is for counting of each symbols and gaining an alphabeth
    for i in range(0, len(arr)):
        if arr[i][0] == val:
            arr[i][1] = arr[i][1] + 1
            return arr
    arr.append([val, int(1)])
    return arr

def retEncodedType(arr, val): #return code according to the symbol
    for i in arr:
        if i[0] == val:
            return i[2]

def main():

    #collecting an input file
    success = False
    while (success != True):
        try:
            inputF = input("Please, type the path to an input file: ")
            iF = open(inputF, 'r', encoding = 'utf-8')
            success = True
        except:
            print("Smth went wrong")
            success = False
    iiF = iF.read()
    
    #populating array with frequency character
    frequenciedArray = [] 
    for i in range(0, len(iiF)):
        addToArray(frequenciedArray, iiF[i])

    frequenciedArray.sort(key = sortingMode, reverse= True) #according to Shannon-Fano method

    #inputing of numeral system's radix
    radix = input("Please enter radix. For example 2 if it is a binary numeral system: ")
    while (radix.isdigit() != True):
        print('It is not valid format of number. Please enter some like 2:')
        radix = input()

    #preparing array for encoding
    for i in range(0, len(frequenciedArray)):
        frequenciedArray[i].append("")

    #directly encoding of symbols
    encodedAlphabet = encodeThisSegment(frequenciedArray, int(radix))

    #printing encoded symbols
    print("Encoded alphabet:")
    print("{0: ^10}   {1: ^10}   {2: ^10}".format("symbol", "quantity", "code"))
    for i in encodedAlphabet:
        print("{0: ^10}   {1: ^10}      {2}".format(i[0], i[1], i[2]))
    
    #outputting into output.txt file encoded text
    of = open("output.txt", 'w', encoding = 'utf-8')
    for i in iiF:
        of.write(retEncodedType(encodedAlphabet, i))
        of.write(" ")

main()

