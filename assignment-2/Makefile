CXXFLAGS := -W -Wall --std=c++11 -shared -fPIC -fvisibility=default -O3 -march=native
TARGETS := libsdes.so
PYTHON := python

all: $(TARGETS)

libsdes.so: sdes.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS)
