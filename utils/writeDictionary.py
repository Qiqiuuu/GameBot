
def writeDictionary(dictionary: dict):
  str = ""
  for key,val in dictionary.items():
      str+=val+ " " +key.mention+"\n"
  return str