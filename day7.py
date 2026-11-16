# total = 0
# for n in range(1,6):
#     total += n

correct_password="admin123"
for attempt in range(1,4):
    password = input("enter your password:")

if password==correct_password:
    print("login successful")