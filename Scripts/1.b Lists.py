# 1.
beta = "Cake"
my_list = ["Frivolous", 42, beta, ["This is a second list, with a number: ", 1], "Peake"]
print(my_list)
my_list.append("Swordfish")
print(my_list)

# 2.

print(my_list[2])
print(my_list[-2])
print(my_list[3][0])

# 3.

print(my_list[0:2])
print(my_list[:2])
print(my_list[2:])
print(my_list[-2])
print(my_list[0::3])

# 4.

var_bol = True
var_bol2 = False
print(bool(var_bol))
print(bool(var_bol2))

# 5.

my_set = {1, 2, 2, 3, 3, 4, "Cake", "Cake"}
print(my_set)

# 6.

my_dict = {1 : "Mervyn", "Peake": 2, "My List" : my_list}
print(my_dict["My List"])