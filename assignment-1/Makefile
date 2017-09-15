CXXFLAGS := -W -Wall --std=c++11 -shared -fPIC -fvisibility=default -O3 -march=native
TARGETS := libsdes.so
PYTHON := python

all: $(TARGETS)

libsdes.so: sdes.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

part1:
	$(PYTHON) vigenere.py --verbose cipher-vigenere.txt

part2: all
	$(PYTHON) task1.py
	$(PYTHON) task2.py
	$(PYTHON) bruteforce.py ctx2.txt
	$(PYTHON) bruteforce.py --sdes ctx1.txt

tasks: part1 part2

clean:
	rm -f $(TARGETS)
