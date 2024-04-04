
def writeDictionary(dictionary: dict):
  str = ""
  print(dictionary)
  for key,val in dictionary.items():
      str+=val+ " " +key.mention+"\n"
  return str