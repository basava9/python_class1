# p=1000
# t=1
# r=10
# si=(p*t*r)/100
# print("simple intrest amount",si)

# kannada=90
# english=80
# hindi=90
# avg=(kannada+english+hindi)/3
# print(avg)

# a=10
# b=20
# print("Before Swapping")
# print("a=",a)
# print("b=",b)
# a,b=b,a
# print("after swapping")
# print("a=",a)
# print("b=",b)

# name=input("Enter your email:")
# password=input("Enter password:")

# num1=float(input("Enter the number1:"))
# num2=float(input("Enter the number2:"))
# print(num1+num2)

# num1=int(input("Enter the number1:"))
# num2=int(input("Enter the number2:"))
# print(num1+num2)

# num1=input("enter the number1:")
# num2=input("enter the number2:")
# print(num1+num2)


# virat_height=1.3
# abd_height=1.0
# if virat_height>abd_height:
#     print("virat is taller")
# else:
#     print("abd is taller")

total=float(input("enter the purchase amount:"))
if total>1000:
    discount=total*0.50
    final_amount=total-discount
    print("Discont applied:",discount)
else:
    print("discount not applied")
    print("pay total amount:",total)