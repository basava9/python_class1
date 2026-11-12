# units=int(input("enter number units used:"))
# if units<=100:
#     bill=units*1
# elif units<=200:
#     bill=100*1 + (units-100)*2
# else:
#     bill=100*1 + 100*2 + (units-200)*5

#     print("electricity bill:",bill)


# a=int(input("enter first angle:"))
# b=int(input("enter second angle:"))
# c=int(input("enter third angle:"))

# if a==b and b==c and c==a:
#     print("equilateral triangle")
# elif a==b or b==c or a==c:
#     print("Isosceles triangle")
# else:
#     print("Scalene triangle")

#Nested if / else

age=17
has_id=True
if age >18:
    if has_id:
        print("entry allowed")
    else:
        print("Show your id card")
else:
    print("Too young for entry")
