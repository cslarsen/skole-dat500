CXXFLAGS := -W -Wall -Wextra -Wconversion -march=native -O3 --std=c++11

run:
	pypy mono.py cipher-mono.txt
