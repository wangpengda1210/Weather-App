import shelve


lib = shelve.open("my_library")
lib["Twilight Saga"] = ["Twilight", "New Moon", "Eclipse", "Breaking Dawn"]

# write your code here
for key in lib:
    print(f'{key}: {lib[key]}')

lib.close()
