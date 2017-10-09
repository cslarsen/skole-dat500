CXXFLAGS := -W -Wall --std=c++11 -fvisibility=default -O3 -march=native
TARGETS := libsdes.so
PYTHON := python

default: run

all: $(TARGETS)

run: all
	$(PYTHON) secure.py

primes: primes.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

libsdes.so: sdes.cpp
	$(CXX) -shared -fPIC $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS)
