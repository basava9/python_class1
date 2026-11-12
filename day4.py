# current_users=int(input("enter number of current users:"))
# new_users=50
# minutes=2
# total_users=current_users + (new_users * minutes)
# if total_users>100:
#     print("lunch new server instance")
# else:
#     print("server stable")

# uptime=97.5
# bill=50000
# if uptime>=99.9:
#     refund=0
# elif uptime>=98:
#     refund=bill*0.10
# else:
#     refund=bill*0.25
#     print("Refund amount:",refund)

weight =float(input("enter the how many kg"))
height=float(input("enter height in meters"))
bmi=weight/(height**2)
if bmi<18.5:
    category="underweight"
elif bmi<25:
    category="Normal"
elif bmi<30:
    category="Overweight"
else:
    category="obese"
    print("Bmi:",bmi)
    print("category:",category)