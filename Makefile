CXXFLAGS := -W -Wall -march=native -O2

run:
	pypy mono.py cipher-mono.txt
