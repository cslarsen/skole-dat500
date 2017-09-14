CXXFLAGS := -W -Wall --std=c++11 -shared -fPIC -fvisibility=default -O3 -march=native
TARGETS := libsdes.so
PYTHON := python

all: $(TARGETS)

libsdes.so: sdes.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

task1:
	$(PYTHON) vigenere.py --verbose cipher-vigenere.txt

task3: all
	$(PYTHON) bruteforce.py ctx2.txt

task2: all
	$(PYTHON) bruteforce.py --sdes ctx1.txt

tasks: task1 task2 task3

clean:
	rm -f $(TARGETS)
