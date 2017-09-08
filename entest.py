from util import *
s = """it was disclosed yesterday that several informal but direct contacts have been made with political representatives of the Viet cong in Moscow"""
s = s.lower()
s = s.replace(" ", "")
print(is_english(s))
