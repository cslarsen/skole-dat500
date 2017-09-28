CXXFLAGS := -W -Wall --std=c++11 -shared -fPIC -fvisibility=default -O3 -march=native
TARGETS := libsdes.so
PYTHON := python

default: run

all: $(TARGETS)

run: all
	$(PYTHON) secure.py

libsdes.so: sdes.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS)
